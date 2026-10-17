# dashboard.py
import json
import os
import random
from datetime import datetime, timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="SOC Command Center | Zero-Trust Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Modern Enterprise Dark CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Header Container */
    .header-panel {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }
    .header-title {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #f8fafc;
        margin: 0;
    }
    .header-sub {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-top: 4px;
        font-weight: 500;
    }
    .status-pill {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #10b981;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        letter-spacing: 0.05em;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .metric-label {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }

    /* Section Headings */
    .section-head {
        font-size: 1.05rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 14px;
        letter-spacing: -0.01em;
    }
</style>
""", unsafe_allow_html=True)

DB_FILE = "zero_trust_datastore.json"

# Sidebar Controls
with st.sidebar:
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        <span style='font-size: 1.2rem; font-weight: 800; color: #f8fafc;'>SOC Controller</span>
    </div>
    <div style='font-size: 0.8rem; color: #64748b; margin-bottom: 20px;'>Real-time Risk Scoring Engine</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    auto_refresh = st.toggle("Live Polling Engine", value=True)
    refresh_rate = st.slider("Polling Interval (sec)", 1, 5, 2)
    
    st.markdown("---")
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #cbd5e1; margin-bottom: 8px;'>Test Threat Injection</div>", unsafe_allow_html=True)
    sim_user = st.selectbox("Assign User Identity", ["internal_ops", "rogue_dev", "session_ext_ip"])
    attack_payload = st.toggle("Inject High-Risk Exploit", value=False)
    
    if st.button("Transmit Packet", use_container_width=True):
        from enforcer_db import datastore
        sim_risk = random.randint(85, 100) if attack_payload else random.randint(10, 28)
        sim_action = "TERMINATE_SESSION_BLOCK_IP" if attack_payload else "ALLOW_REQUEST"
        sim_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": sim_user,
            "client_ip": "104.244.42.1" if attack_payload else "192.168.4.15",
            "endpoint": "/admin/vault/access" if attack_payload else "/api/feed",
            "payload_kb": 18.5 if attack_payload else 0.32,
            "inter_arrival_sec": 0.01 if attack_payload else 1.4
        }
        datastore.apply_policy(
            user_id=sim_user,
            client_ip=sim_event["client_ip"],
            risk_score=sim_risk,
            decision=sim_action,
            details=sim_event
        )
        st.toast(f"Event logged: {sim_action}", icon="🚨" if attack_payload else "✅")

# Data fetch
if not os.path.exists(DB_FILE):
    st.warning("Telemetry file nahi mila. Pehle `proxy_engine.py` run karein.")
    st.stop()

with open(DB_FILE, "r") as f:
    try:
        raw_db = json.load(f)
    except Exception:
        raw_db = {"sessions": {}, "audit_logs": []}

sessions = raw_db.get("sessions", {})
audit_logs = raw_db.get("audit_logs", [])
df_logs = pd.DataFrame(audit_logs) if audit_logs else pd.DataFrame()

# Clean Executive Header
st.markdown("""
<div class="header-panel">
    <div>
        <h1 class="header-title">Zero-Trust SOC Command Center</h1>
        <div class="header-sub">Continuous Behavioral Telemetry & Autonomous Threat Quarantine</div>
    </div>
    <div class="status-pill">
        <span style="font-size: 10px;">●</span> ENGINE ACTIVE
    </div>
</div>
""", unsafe_allow_html=True)

# Metrics Grid
total_ev = len(audit_logs)
blocked_ev = sum(1 for log in audit_logs if log.get("action_taken") == "TERMINATE_SESSION_BLOCK_IP")
mfa_ev = sum(1 for log in audit_logs if log.get("action_taken") == "REQUIRE_STEPUP_MFA")
allowed_ev = sum(1 for log in audit_logs if log.get("action_taken") == "ALLOW_REQUEST")
quar_n = sum(1 for s in sessions.values() if s.get("status") == "BLOCKED")

m1, m2, m3, m4, m5 = st.columns(5)
m1.markdown(f'<div class="metric-card"><div class="metric-label">Total Ingested</div><div class="metric-val" style="color: #38bdf8;">{total_ev}</div></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-card"><div class="metric-label">Access Granted</div><div class="metric-val" style="color: #34d399;">{allowed_ev}</div></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-card"><div class="metric-label">MFA Challenges</div><div class="metric-val" style="color: #fbbf24;">{mfa_ev}</div></div>', unsafe_allow_html=True)
m4.markdown(f'<div class="metric-card"><div class="metric-label">Threats Blocked</div><div class="metric-val" style="color: #f87171;">{blocked_ev}</div></div>', unsafe_allow_html=True)
m5.markdown(f'<div class="metric-card"><div class="metric-label">Quarantined Sessions</div><div class="metric-val" style="color: #cbd5e1;">{quar_n}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Visuals Area
c1, c2 = st.columns([1, 1.45])

with c1:
    st.markdown('<div class="section-head">Enforcement Policy Ratio</div>', unsafe_allow_html=True)
    if not df_logs.empty:
        counts = df_logs["action_taken"].value_counts().reset_index()
        counts.columns = ["Action", "Frequency"]
        
        fig_ring = px.pie(
            counts,
            values="Frequency",
            names="Action",
            hole=0.62,
            color="Action",
            color_discrete_map={
                "ALLOW_REQUEST": "#10b981",
                "REQUIRE_STEPUP_MFA": "#f59e0b",
                "TERMINATE_SESSION_BLOCK_IP": "#ef4444"
            }
        )
        fig_ring.update_traces(
            textposition='outside',
            textinfo='percent+label',
            textfont=dict(family="Plus Jakarta Sans", size=11, color="#cbd5e1"),
            marker=dict(line=dict(color='#0b0f19', width=2))
        )
        fig_ring.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(family="Plus Jakarta Sans")
        )
        st.plotly_chart(fig_ring, use_container_width=True)
    else:
        st.info("No logs present.")

with c2:
    st.markdown('<div class="section-head">Live Threat Anomaly Trend (Last 45 Events)</div>', unsafe_allow_html=True)
    if not df_logs.empty:
        seq = df_logs.tail(45).reset_index()
        
        fig_stream = go.Figure()
        fig_stream.add_trace(go.Scatter(
            x=seq.index,
            y=seq["risk_score"],
            mode="lines+markers",
            line=dict(color="#38bdf8", width=2),
            marker=dict(
                size=5,
                color=seq["risk_score"],
                colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
                showscale=False
            ),
            fill='tozeroy',
            fillcolor='rgba(56, 189, 248, 0.06)',
            name="Risk Score"
        ))
        fig_stream.add_hline(
            y=75,
            line_dash="dot",
            line_color="#ef4444",
            annotation_text="Isolation Threshold (75)",
            annotation_position="top left",
            annotation_font=dict(family="Plus Jakarta Sans", color="#ef4444", size=10)
        )
        
        fig_stream.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans"),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', range=[0, 105], title="Risk (0-100)")
        )
        st.plotly_chart(fig_stream, use_container_width=True)
    else:
        st.info("Awaiting telemetry flow...")

st.markdown("---")

# Session Registry & Audit Logs Tables
g1, g2 = st.columns([1, 1.35])

with g1:
    st.markdown('<div class="section-head">Registered Identities & Status</div>', unsafe_allow_html=True)
    if sessions:
        identity_cards = []
        for ident, info in sessions.items():
            status = info.get("status", "UNKNOWN").replace("_", " ")
            score = info.get("risk_score", 0)
            identity_cards.append({
                "User": ident,
                "Threat Level": f"{score}/100",
                "Status": status
            })
        st.dataframe(pd.DataFrame(identity_cards), use_container_width=True)
    else:
        st.caption("No registered identity nodes.")

with g2:
    st.markdown('<div class="section-head">Latest Security Audit Trail</div>', unsafe_allow_html=True)
    if not df_logs.empty:
        logs_table = df_logs[["timestamp", "user_id", "client_ip", "risk_score", "action_taken"]].tail(8).iloc[::-1]
        st.dataframe(logs_table, use_container_width=True)
    else:
        st.caption("No audit logs recorded.")

# Auto-refresh loop
if auto_refresh:
    import time
    time.sleep(refresh_rate)
    st.rerun()