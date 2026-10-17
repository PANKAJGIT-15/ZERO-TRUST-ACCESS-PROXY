# enforcer_db.py
import json
import os
from datetime import datetime

DB_FILE = "zero_trust_datastore.json"

class SecurityStore:
    def __init__(self):
        if not os.path.exists(DB_FILE):
            self.data = {"sessions": {}, "audit_logs": []}
            self._save()
        else:
            with open(DB_FILE, "r") as f:
                self.data = json.load(f)

    def _save(self):
        with open(DB_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def apply_policy(self, user_id, client_ip, risk_score, decision, details):
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "client_ip": client_ip,
            "risk_score": risk_score,
            "action_taken": decision,
            "details": details
        }
        self.data["audit_logs"].append(audit_entry)

        if decision == "TERMINATE_SESSION_BLOCK_IP":
            self.data["sessions"][user_id] = {
                "status": "BLOCKED",
                "risk_score": risk_score,
                "reason": "Anomaly Threshold Exceeded",
                "updated_at": datetime.utcnow().isoformat()
            }
        elif decision == "REQUIRE_STEPUP_MFA":
            self.data["sessions"][user_id] = {
                "status": "MFA_CHALLENGE_REQUIRED",
                "risk_score": risk_score,
                "updated_at": datetime.utcnow().isoformat()
            }
        else:
            self.data["sessions"][user_id] = {
                "status": "ACTIVE_VERIFIED",
                "risk_score": risk_score,
                "last_verified": datetime.utcnow().isoformat()
            }

        self._save()

datastore = SecurityStore()