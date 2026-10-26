# dashboard.py
import json
import os
import random
import time
from datetime import datetime, timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AEGIS // Zero-Trust Cyber Defense Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Modern Glassmorphic Dark SOC Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    .stApp {
        background-color: #040711;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.08) 0px, transparent 40%),
            radial-gradient(circle at 85% 85%, rgba(99, 102, 241, 0.06) 0px, transparent 40%);
        color: #f8fafc;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #080d1a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    .sidebar-brand-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 20px;
    }
    .side-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .side-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #38bdf8;
        font-weight: 600;
    }

    /* Top Executive HUD Bar */
    .top-hud-bar {
        background: rgba(13, 21, 38, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 14px 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(20px);
        margin-bottom: 18px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.45);
    }
    .hud-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hud-icon {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 0 16px rgba(14, 165, 233, 0.4);
    }
    .hud-title-text {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .hud-subtitle-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #64748b;
        letter-spacing: 0.06em;
    }
    .hud-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 6px 14px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    /* Metric Cards */
    .kpi-card {
        background: rgba(13, 21, 38, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px 18px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(14px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.3);
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
    }
    .kpi-blue::before { background: #38bdf8; }
    .kpi-green::before { background: #10b981; }
    .kpi-amber::before { background: #f59e0b; }
    .kpi-rose::before { background: #f43f5e; }
    .kpi-purple::before { background: #a855f7; }

    .kpi-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.95rem;
        font-weight: 700;
        margin-top: 4px;
        line-height: 1;
    }

    /* Main Content Panels */
    .glass-box {
        background: rgba(13, 21, 38, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px 20px;
        backdrop-filter: blur(16px);
        margin-bottom: 16px;
    }
    .box-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 10px;
        margin-bottom: 14px;
    }
    .box-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .box-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #64748b;
    }

    /* Identity Node Badges */
    .node-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 14px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 600;
        margin: 4px;
    }
    .badge-allow {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
    }
    .badge-mfa {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.35);
        color: #fbbf24;
    }
    .badge-block {
        background: rgba(244, 63, 94, 0.1);
        border: 1px solid rgba(244, 63, 94, 0.35);
        color: #fb7185;
    }

    /* Terminal Forensic Feed */
    .terminal-feed {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        max-height: 260px;
        overflow-y: auto;
    }
    .term-line {
        display: grid;
        grid-template-columns: 150px 120px 120px 80px 1fr;
        padding: 8px 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        align-items: center;
    }
    .term-line:hover {
        background: rgba(255, 255, 255, 0.02);
    }
</style>
""", unsafe_allow_html=True)

DB_FILE = "zero_trust_datastore.json"

def load_security_db():
    if not os.path.exists(DB_FILE):
        return {"sessions": {}, "audit_logs": []}
    for _ in range(3):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            time.sleep(0.04)
    return {"sessions": {}, "audit_logs": []}

raw_db = load_security_db()
sessions = raw_db.get("sessions", {})
audit_logs = raw_db.get("audit_logs", [])
df_logs = pd.DataFrame(audit_logs) if audit_logs else pd.DataFrame()

# ==========================================
# SIDEBAR: ADVANCED OPS & CONTROL
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="side-title">AEGIS // SEC-OPS</div>
        <div class="side-badge">v2.5 • ZERO-TRUST MESH</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-family: JetBrains Mono; font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-bottom: 4px;'>OPERATIONS DECK</div>", unsafe_allow_html=True)
    active_screen = st.radio(
        "Active Deck",
        [
            "Threat Radar & Global Mesh",
            "Red-Team Threat Injector",
            "Quarantine Registry",
            "Full Forensic Audit Stream"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<div style='font-family: JetBrains Mono; font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-bottom: 4px;'>SYSTEM POLICIES</div>", unsafe_allow_html=True)
    auto_refresh = st.toggle("Active Heartbeat Loop", value=True)
    refresh_rate = st.slider("Sampling Frequency (sec)", 1, 5, 2)
    risk_threshold = st.slider("Isolation Ceiling (Risk Threshold)", 60, 95, 75)
    
    st.markdown("---")
    st.markdown("<div style='font-family: JetBrains Mono; font-size: 0.72rem; color: #94a3b8; font-weight: 600; margin-bottom: 4px;'>NODE TELEMETRY FILTER</div>", unsafe_allow_html=True)
    all_users = list(sessions.keys()) if sessions else ["All Nodes"]
    filter_user = st.selectbox("Inspect Target Node", ["All Nodes"] + all_users)
    
    st.markdown("---")
    st.caption("Engine: Pure Python Async FIFO • Standard: NIST SP800-207 Zero-Trust")

# Filtering df if selected
if filter_user != "All Nodes" and not df_logs.empty:
    df_filtered = df_logs[df_logs["user_id"] == filter_user]
else:
    df_filtered = df_logs

# Top Header Bar
st.markdown("""
<div class="top-hud-bar">
    <div class="hud-brand">
        <div class="hud-icon">🛡️</div>
        <div>
            <div class="hud-title-text">AEGIS // ZERO-TRUST COMMAND</div>
            <div class="hud-subtitle-text">CONTINUOUS BEHAVIORAL TELEMETRY & ADAPTIVE MICRO-SEGMENTATION</div>
        </div>
    </div>
    <div class="hud-pill">
        <span class="pulse-dot"></span>
        <span>DEFENSE MESH ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# KPI Metric Cards
total_ev = len(df_logs)
blocked_ev = sum(1 for log in audit_logs if log.get("action_taken") == "TERMINATE_SESSION_BLOCK_IP")
mfa_ev = sum(1 for log in audit_logs if log.get("action_taken") == "REQUIRE_STEPUP_MFA")
allowed_ev = sum(1 for log in audit_logs if log.get("action_taken") == "ALLOW_REQUEST")
quar_n = sum(1 for s in sessions.values() if s.get("status") == "BLOCKED")

k1, k2, k3, k4, k5 = st.columns(5)
k1.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-tag">Total Ingested</div><div class="kpi-val" style="color:#38bdf8;">{total_ev}</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi-card kpi-green"><div class="kpi-tag">Access Permitted</div><div class="kpi-val" style="color:#10b981;">{allowed_ev}</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi-card kpi-amber"><div class="kpi-tag">MFA Challenges</div><div class="kpi-val" style="color:#f59e0b;">{mfa_ev}</div></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi-card kpi-rose"><div class="kpi-tag">Threats Blocked</div><div class="kpi-val" style="color:#f43f5e;">{blocked_ev}</div></div>', unsafe_allow_html=True)
k5.markdown(f'<div class="kpi-card kpi-purple"><div class="kpi-tag">Isolated Nodes</div><div class="kpi-val" style="color:#c084fc;">{quar_n}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# VIEW 1: THREAT RADAR & GLOBAL MESH
# ==========================================
if active_screen == "Threat Radar & Global Mesh":
    col_l, col_r = st.columns([1.1, 2.2])

    with col_l:
        # Threat Gauge
        st.markdown("""
        <div class="glass-box">
            <div class="box-head">
                <div class="box-title">⚡ Current Threat Index</div>
                <div class="box-meta">GAUSSIAN ESTIMATOR</div>
            </div>
        """, unsafe_allow_html=True)
        
        cur_score = df_filtered.iloc[-1]["risk_score"] if not df_filtered.empty else 0
        gauge_color = "#f43f5e" if cur_score >= risk_threshold else "#f59e0b" if cur_score >= 45 else "#10b981"
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=cur_score,
            number={'font': {'family': "JetBrains Mono", 'size': 44, 'color': "#ffffff"}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#475569", 'tickfont': {'family': "JetBrains Mono", 'size': 9, 'color': "#94a3b8"}},
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'bgcolor': "rgba(15, 23, 42, 0.4)",
                'steps': [
                    {'range': [0, 45], 'color': 'rgba(16, 185, 129, 0.1)'},
                    {'range': [45, risk_threshold], 'color': 'rgba(245, 158, 11, 0.1)'},
                    {'range': [risk_threshold, 100], 'color': 'rgba(244, 63, 94, 0.15)'}
                ],
                'threshold': {'line': {'color': "#f43f5e", 'width': 3}, 'value': risk_threshold}
            }
        ))
        fig_gauge.update_layout(height=210, margin=dict(l=15, r=15, t=35, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

        # Monitored Identity Badges
        st.markdown("""
        <div class="glass-box">
            <div class="box-head">
                <div class="box-title">👥 Monitored Identity Nodes</div>
                <div class="box-meta">ACTIVE SESSIONS</div>
            </div>
        """, unsafe_allow_html=True)
        if sessions:
            badges_html = ""
            for ident, s in sessions.items():
                status = s.get("status", "ACTIVE")
                b_cls = "badge-block" if status == "BLOCKED" else "badge-mfa" if "MFA" in status else "badge-allow"
                badges_html += f'<div class="node-badge {b_cls}"><span>●</span> {ident} <span style="opacity:0.65;">[{s.get("risk_score", 0)}]</span></div>'
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.caption("No registered identity nodes.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        # Waveform Stream
        st.markdown("""
        <div class="glass-box">
            <div class="box-head">
                <div class="box-title">📈 Adaptive Risk Stream Telemetry</div>
                <div class="box-meta">SLIDING WINDOW (LAST 45 EVENTS)</div>
            </div>
        """, unsafe_allow_html=True)
        
        if not df_filtered.empty:
            stream_tail = df_filtered.tail(45).reset_index()
            fig_stream = go.Figure()
            fig_stream.add_trace(go.Scatter(
                x=stream_tail.index, y=stream_tail["risk_score"],
                mode="lines+markers",
                line=dict(color="#38bdf8", width=2.5),
                marker=dict(size=5, color=stream_tail["risk_score"], colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#f43f5e"]]),
                fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.05)'
            ))
            fig_stream.add_hline(
                y=risk_threshold, line_dash="dash", line_color="#f43f5e",
                annotation_text=f"KILL-SWITCH ({risk_threshold})",
                annotation_font=dict(family="JetBrains Mono", size=9, color="#f43f5e")
            )
            fig_stream.update_layout(
                height=210, margin=dict(l=10, r=10, t=15, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(range=[0, 105], showgrid=True, gridcolor='rgba(255,255,255,0.04)', tickfont=dict(family="JetBrains Mono", size=9, color="#64748b")),
                xaxis=dict(showgrid=False, showticklabels=False)
            )
            st.plotly_chart(fig_stream, width='stretch')
        else:
            st.caption("Waiting for stream telemetry...")
        st.markdown('</div>', unsafe_allow_html=True)

        # Global Geo Map
        st.markdown("""
        <div class="glass-box">
            <div class="box-head">
                <div class="box-title">🌐 Global Ingestion Origins</div>
                <div class="box-meta">VELOCITY / IMPOSSIBLE TRAVEL CHECK</div>
            </div>
        """, unsafe_allow_html=True)
        
        geo_data = pd.DataFrame([
            {"lat": 18.9894, "lon": 72.8300, "location": "Mumbai Local Subnet", "state": "Verified", "weight": 14},
            {"lat": 37.7749, "lon": -122.4194, "location": "San Francisco Datacenter", "state": "Exploit Burst", "weight": 24},
            {"lat": 52.3676, "lon": 4.9041, "location": "Amsterdam Anonymous Relay", "state": "Tor Node", "weight": 18}
        ])
        fig_map = px.scatter_geo(
            geo_data, lat="lat", lon="lon", hover_name="location", size="weight",
            color="state",
            color_discrete_map={
                "Verified": "#10b981",
                "Tor Node": "#f59e0b",
                "Exploit Burst": "#f43f5e"
            }
        )
        fig_map.update_geos(
            bgcolor="rgba(0,0,0,0)",
            showcountries=True, countrycolor="#1e293b",
            showocean=True, oceancolor="#040711",
            showland=True, landcolor="#0f172a",
            showlakes=False
        )
        fig_map.update_layout(
            height=190, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )
        st.plotly_chart(fig_map, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

    # Forensic Feed
    st.markdown("""
    <div class="glass-box">
        <div class="box-head">
            <div class="box-title">📋 Live Forensic Audit Feed (Latest Ingested Packets)</div>
            <div class="box-meta">IMMUTABLE LOGS</div>
        </div>
        <div class="terminal-feed">
    """, unsafe_allow_html=True)

    if not df_filtered.empty:
        log_rows_html = ""
        for _, row in df_filtered.tail(8).iloc[::-1].iterrows():
            act = row.get("action_taken", "UNKNOWN")
            act_col = "#34d399" if "ALLOW" in act else "#fbbf24" if "MFA" in act else "#fb7185"
            ts = str(row.get("timestamp", ""))[:19].replace("T", " ")
            log_rows_html += f"""
            <div class="term-line">
                <span style="color:#64748b;">{ts}</span>
                <span style="color:#cbd5e1; font-weight:600;">{row.get('user_id')}</span>
                <span style="color:#38bdf8;">{row.get('client_ip')}</span>
                <span style="color:#ffffff;">SCORE: {row.get('risk_score')}</span>
                <span style="color:{act_col}; font-weight:700;">{act}</span>
            </div>
            """
        st.markdown(log_rows_html + "</div></div>", unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#64748b;">No security logs recorded.</div></div></div>', unsafe_allow_html=True)

# ==========================================
# VIEW 2: RED-TEAM THREAT INJECTOR
# ==========================================
elif active_screen == "Red-Team Threat Injector":
    st.markdown("""
    <div class="glass-box">
        <div class="box-head">
            <div class="box-title">⚡ Adversarial Threat Injection Sandbox</div>
            <div class="box-meta">MANUAL EXPLOIT SIMULATION</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_inj1, col_inj2 = st.columns([1.2, 1])
    with col_inj1:
        target_usr = st.selectbox("Assign Identity Node", ["user_alpha", "user_beta", "attacker_x", "rogue_dev", "session_ext_ip"])
        threat_profile = st.selectbox(
            "Select Attack Vector Signature",
            [
                "Normative User Flow (/api/dashboard)",
                "Automated High-Frequency Micro-Burst (/auth/refresh)",
                "Impossible Travel Velocity Jump (Dual Subnet / Tor)",
                "Privileged Route Infiltration (/admin/database/dump)"
            ]
        )
        
        if st.button("🚀 TRANSMIT ATTACK VECTOR", width='stretch'):
            from enforcer_db import datastore
            if "Normative" in threat_profile:
                risk = random.randint(12, 22)
                act = "ALLOW_REQUEST"
                ip = "192.168.1.10"
                ep = "/api/v2/metrics"
            elif "Micro-Burst" in threat_profile:
                risk = random.randint(52, 68)
                act = "REQUIRE_STEPUP_MFA"
                ip = "192.168.1.10"
                ep = "/auth/refresh"
            elif "Impossible" in threat_profile:
                risk = 94
                act = "TERMINATE_SESSION_BLOCK_IP"
                ip = "185.220.101.5"
                ep = "/vault/credentials"
            else:
                risk = 100
                act = "TERMINATE_SESSION_BLOCK_IP"
                ip = "45.33.32.156"
                ep = "/admin/database/dump"
                
            datastore.apply_policy(
                user_id=target_usr,
                client_ip=ip,
                risk_score=risk,
                decision=act,
                details={"endpoint": ep, "signature": threat_profile}
            )
            st.toast(f"Policy Action Triggered: {act}", icon="🚨" if risk >= risk_threshold else "✅")
            
    with col_inj2:
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.4); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:16px;">
            <div style="font-family:'Plus Jakarta Sans'; font-size:0.95rem; font-weight:700; margin-bottom:8px; color:#ffffff;">Policy Threshold Matrix</div>
            <div style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#94a3b8; line-height:1.7;">
                <b style="color:#10b981;">• RISK &lt; 45:</b> ALLOW_REQUEST (Normative Activity)<br>
                <b style="color:#f59e0b;">• RISK 45–{risk_threshold-1}:</b> REQUIRE_STEPUP_MFA (Challenge Prompt)<br>
                <b style="color:#f43f5e;">• RISK &ge; {risk_threshold}:</b> TERMINATE_SESSION_BLOCK_IP (Kill-Switch)
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 3: QUARANTINE REGISTRY
# ==========================================
elif active_screen == "Quarantine Registry":
    st.markdown("""
    <div class="glass-box">
        <div class="box-head">
            <div class="box-title">🔒 Active Identity Registry & Micro-Segmentation</div>
            <div class="box-meta">SESSION STATE PERSISTENCE</div>
        </div>
    """, unsafe_allow_html=True)
    if sessions:
        records = []
        for ident, s in sessions.items():
            records.append({
                "Identity Node": ident,
                "Threat Level": f"{s.get('risk_score', 0)} / 100",
                "Policy State": s.get("status", "ACTIVE"),
                "Context Reason": s.get("reason", "Normative Baseline"),
                "Last Active": s.get("updated_at", s.get("last_verified", "N/A"))
            })
        st.dataframe(pd.DataFrame(records), width='stretch')
    else:
        st.info("No identity records active.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# VIEW 4: FULL FORENSIC AUDIT STREAM
# ==========================================
elif active_screen == "Full Forensic Audit Stream":
    st.markdown("""
    <div class="glass-box">
        <div class="box-head">
            <div class="box-title">📋 Full Forensic Audit Ledger</div>
            <div class="box-meta">COMPLETE ATOMIC LOGS</div>
        </div>
    """, unsafe_allow_html=True)
    if not df_filtered.empty:
        log_records = df_filtered[["timestamp", "user_id", "client_ip", "risk_score", "action_taken"]].tail(50).iloc[::-1]
        st.dataframe(log_records, width='stretch')
    else:
        st.info("Audit log is currently empty.")
    st.markdown('</div>', unsafe_allow_html=True)

# Heartbeat loop
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()