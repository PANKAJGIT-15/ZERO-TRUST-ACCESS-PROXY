# proxy_engine.py
import random
import threading
import time
from datetime import datetime, timezone
import numpy as np
from sklearn.ensemble import IsolationForest

from broker import broker
from enforcer_db import datastore

TOPIC = "user-access-events"
broker.create_topic(TOPIC)

# Multivariate Baseline Training:
# Features: [payload_kb, inter_arrival_sec, sensitive_route_flag, burst_frequency_score]
train_features = np.array([
    [0.5, 1.2, 0, 1], [0.8, 1.0, 0, 1], [0.2, 2.0, 0, 1], [0.4, 0.9, 0, 1],
    [1.1, 1.5, 0, 2], [0.6, 1.1, 0, 1], [0.3, 0.8, 0, 1], [0.9, 1.4, 0, 1],
    [1.2, 1.8, 0, 1], [0.7, 1.3, 0, 1], [1.0, 1.6, 0, 2], [0.5, 1.0, 0, 1]
])
clf = IsolationForest(contamination=0.08, random_state=42)
clf.fit(train_features)

# Rolling cache to detect rapid subnet hopping / impossible travel
user_session_cache = {}

def calculate_behavioral_risk(user_id, client_ip, features):
    now = time.time()
    
    # 1. Unsupervised Isolation Forest Anomaly Detection
    anomaly_prediction = clf.predict([features])[0]
    base_score = 12 if anomaly_prediction == 1 else 55

    # 2. Privileged Route Penalty (/admin, /vault, /dump)
    if features[2] == 1:
        base_score += 35

    # 3. Micro-Burst Machine Automation Penalty
    if features[1] < 0.08:
        base_score += 25

    # 4. Data Exfiltration / Large Payload Penalty
    if features[0] > 12.0:
        base_score += 15

    # 5. Impossible Travel & Geo-Velocity Engine
    if user_id in user_session_cache:
        last_seen, last_ip = user_session_cache[user_id]
        time_delta = now - last_seen
        # Agar identical user ka IP under 5 seconds me completely jump ho jaye
        if last_ip != client_ip and time_delta < 5.0:
            base_score = max(base_score, 95)

    user_session_cache[user_id] = (now, client_ip)
    return min(base_score, 100)

def producer_worker():
    users = ['user_alpha', 'user_beta', 'attacker_x', 'compromised_dev', 'session_ext_ip']
    routes = ['/api/dashboard', '/api/profile', '/admin/database/dump', '/vault/secrets']

    while True:
        user = random.choice(users)
        
        if user == 'attacker_x':
            route = '/admin/database/dump'
            payload = random.uniform(9.0, 26.0)
            interval = random.uniform(0.01, 0.04)
            ip = '45.33.32.156'
            burst_score = 10
        elif user in ['compromised_dev', 'session_ext_ip']:
            # Simulating anomalous IP velocity jump
            route = random.choice(routes)
            payload = random.uniform(1.2, 4.0)
            interval = random.uniform(0.2, 0.8)
            ip = random.choice(['192.168.1.10', '185.220.101.5'])
            burst_score = 6
        else:
            route = random.choice(routes[:2])
            payload = random.uniform(0.2, 1.4)
            interval = random.uniform(0.9, 1.8)
            ip = '192.168.1.10'
            burst_score = 1

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user,
            "client_ip": ip,
            "endpoint": route,
            "payload_kb": round(payload, 2),
            "inter_arrival_sec": round(interval, 3),
            "burst_freq": burst_score
        }
        broker.produce(TOPIC, event)
        time.sleep(interval)

def consumer_engine():
    print("=" * 75)
    print("AEGIS ZERO-TRUST ACCESS PROXY ENGINE (ACTIVE STREAM RUNNING)")
    print("=" * 75)

    while True:
        event = broker.consume(TOPIC)
        if not event:
            continue

        route_flag = 1 if any(p in event["endpoint"] for p in ["admin", "vault", "dump"]) else 0
        features = [
            event["payload_kb"],
            event["inter_arrival_sec"],
            route_flag,
            event.get("burst_freq", 1)
        ]

        risk = calculate_behavioral_risk(event["user_id"], event["client_ip"], features)

        if risk >= 75:
            decision = "TERMINATE_SESSION_BLOCK_IP"
            action_tag = "\033[91m[QUARANTINED]\033[0m"
        elif risk >= 45:
            decision = "REQUIRE_STEPUP_MFA"
            action_tag = "\033[93m[CHALLENGE MFA]\033[0m"
        else:
            decision = "ALLOW_REQUEST"
            action_tag = "\033[92m[PERMITTED]\033[0m"

        datastore.apply_policy(
            user_id=event["user_id"],
            client_ip=event["client_ip"],
            risk_score=risk,
            decision=decision,
            details=event
        )

        print(f"{action_tag} Node: {event['user_id']:<17} | Path: {event['endpoint']:<22} | Score: {risk}/100")

if __name__ == "__main__":
    t1 = threading.Thread(target=producer_worker, daemon=True)
    t1.start()
    try:
        consumer_engine()
    except KeyboardInterrupt:
        print("\n\033[93m[STOPPED] Zero-Trust Engine terminated gracefully by user.\033[0m")