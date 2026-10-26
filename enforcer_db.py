# enforcer_db.py
import json
import os
import time
from datetime import datetime, timezone

DB_FILE = "zero_trust_datastore.json"

class SecurityStore:
    def __init__(self):
        self._ensure_datastore()

    def _ensure_datastore(self):
        if not os.path.exists(DB_FILE):
            self.data = {"sessions": {}, "audit_logs": []}
            self._save()
        else:
            self._load()

    def _load(self):
        try:
            with open(DB_FILE, "r") as f:
                self.data = json.load(f)
        except Exception:
            self.data = {"sessions": {}, "audit_logs": []}

    def _save(self):
        temp_file = f"{DB_FILE}.tmp"
        try:
            with open(temp_file, "w") as f:
                json.dump(self.data, f, indent=2)
            os.replace(temp_file, DB_FILE)
        except Exception:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

    def apply_policy(self, user_id, client_ip, risk_score, decision, details):
        self._load()
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "client_ip": client_ip,
            "risk_score": risk_score,
            "action_taken": decision,
            "details": details
        }
        self.data["audit_logs"].append(audit_entry)

        # File size control (last 200 logs only)
        if len(self.data["audit_logs"]) > 200:
            self.data["audit_logs"] = self.data["audit_logs"][-200:]

        if decision == "TERMINATE_SESSION_BLOCK_IP":
            self.data["sessions"][user_id] = {
                "status": "BLOCKED",
                "risk_score": risk_score,
                "reason": "Anomaly Threshold Exceeded",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        elif decision == "REQUIRE_STEPUP_MFA":
            self.data["sessions"][user_id] = {
                "status": "MFA_CHALLENGE_REQUIRED",
                "risk_score": risk_score,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        else:
            self.data["sessions"][user_id] = {
                "status": "ACTIVE_VERIFIED",
                "risk_score": risk_score,
                "last_verified": datetime.now(timezone.utc).isoformat()
            }

        self._save()

datastore = SecurityStore()