# proxy_engine.py
import random
import threading
import time
from datetime import datetime
import numpy as np
from sklearn.ensemble import IsolationForest

from broker import broker
from enforcer_db import datastore

TOPIC = "user-access-events"
broker.create_topic(TOPIC)

# Train baseline ML Anomaly Detection Model
# Features: [payload_size_kb, inter_arrival_time_sec, sensitive_route_flag]
train_features = np.array([
    [0.5, 1.2, 0], [0.8, 1.0, 0], [0.2, 2.0, 0], [0.4, 0.9, 0],
    [1.1, 1.5, 0], [0.6, 1.1, 0], [0.3, 0.8, 0], [0.9, 1.4, 0]
])
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(train_features)

def calculate_risk_score(features, raw_event):
    # ML Anomaly calculation (-1 indicates anomaly)
    anomaly_prediction = clf.predict([features])[0]
    base_score = 15 if anomaly_prediction == 1 else 60

    # Rule-based threat intelligence weightings
    if features[2] == 1:  # Admin/restricted route
        base_score += 30
    if features[1] < 0.1:  # Rapid burst
        base_score += 20
    if features[0] > 10.0: # Huge payload
        base_score += 15

    return min(base_score, 100)

def producer_worker():
    users = ['user_alpha', 'user_beta', 'attacker_x']
    routes = ['/api/dashboard', '/api/profile', '/admin/database/dump']
    
    while True:
        user = random.choice(users)
        if user == 'attacker_x':
            route = '/admin/database/dump'
            payload = random.uniform(8.0, 25.0)
            interval = random.uniform(0.01, 0.05)
            ip = '45.33.32.156'
        else:
            route = random.choice(routes[:2])
            payload = random.uniform(0.2, 1.5)
            interval = random.uniform(0.8, 1.8)
            ip = '192.168.1.10'

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user,
            "client_ip": ip,
            "endpoint": route,
            "payload_kb": round(payload, 2),
            "inter_arrival_sec": round(interval, 3)
        }
        broker.produce(TOPIC, event)
        time.sleep(interval)

def consumer_engine():
    print("=" * 65)
    print("ZERO-TRUST ACCESS PROXY ENGINE (RUNNING)")
    print("=" * 65)
    
    while True:
        event = broker.consume(TOPIC)
        if not event:
            continue

        route_flag = 1 if "admin" in event["endpoint"] else 0
        features = [event["payload_kb"], event["inter_arrival_sec"], route_flag]
        
        risk = calculate_risk_score(features, event)
        
        if risk >= 75:
            decision = "TERMINATE_SESSION_BLOCK_IP"
            action_tag = "\033[91m[BLOCKED]\033[0m"
        elif risk >= 45:
            decision = "REQUIRE_STEPUP_MFA"
            action_tag = "\033[93m[CHALLENGE MFA]\033[0m"
        else:
            decision = "ALLOW_REQUEST"
            action_tag = "\033[92m[ALLOWED]\033[0m"

        datastore.apply_policy(
            user_id=event["user_id"],
            client_ip=event["client_ip"],
            risk_score=risk,
            decision=decision,
            details=event
        )

        print(f"{action_tag} User: {event['user_id']:<12} | Route: {event['endpoint']:<22} | Risk: {risk}/100")

if __name__ == "__main__":
    t1 = threading.Thread(target=producer_worker, daemon=True)
    t1.start()
    consumer_engine()