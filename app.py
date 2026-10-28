import streamlit as st
import numpy as np
import time

st.set_page_config(
    page_title="EV Battery Live Monitoring",
    page_icon="🚗",
    layout="wide"
)

# Custom High-Tech Automotive Theme & Mechanical Styling
st.markdown("""
<style>
    /* Automotive Vehicle & Mechanical Tools HD Background */
    .stApp {
        background: linear-gradient(rgba(18, 24, 27, 0.88), rgba(18, 24, 27, 0.94)),
                    url('https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Main Container Card: Fair White with Subtle Glassmorphism */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
        position: relative;
    }

    .metric-sublabel {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 4px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #1E293B;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    /* Section Headers: Olive Green Accent */
    .section-header {
        font-size: 19px;
        font-weight: 800;
        color: #FAFAFA;
        margin-top: 22px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Status Badges */
    .status-badge-good {
        display: inline-flex;
        align-items: center;
        background-color: #556B2F;
        color: #FAFAFA;
        font-weight: 800;
        font-size: 14px;
        padding: 8px 20px;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0 0 10px rgba(85, 107, 47, 0.5);
    }

    .status-badge-warn {
        display: inline-flex;
        align-items: center;
        background-color: #FFE4E8;
        border: 1.5px solid #FF6584;
        color: #9F1239;
        font-weight: 800;
        font-size: 14px;
        padding: 8px 20px;
        border-radius: 20px;
        margin-top: 20px;
    }

    /* Mechanical Rig Header */
    .top-header {
        background: linear-gradient(135deg, #556B2F, #6B8E23);
        border: 2px solid #84A346;
        color: #FAFAFA;
        padding: 18px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .top-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 1px;
    }
    
    .top-header p {
        margin: 5px 0 0 0;
        font-size: 14px;
        opacity: 0.95;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#556B2F; margin-bottom:0;'>🚗 EV BATTERY RIG</h2>", unsafe_allow_html=True)
    st.caption("Telemetry Diagnostics Console")
    
    st.radio(
        "Navigation",
        ["Live Dashboard", "Telemetry Log", "AI Health (SOH)", "Alerts & Safety", "Settings"],
        index=0
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background:#E0F2FE; border-left:4px solid #38BDF8; padding:8px 12px; border-radius:6px; margin-bottom:10px; font-weight:700; color:#0284C7; font-size:13px;'>
            🟢 AI Inference: ACTIVE
        </div>
        <div style='background:#FFE4E8; border-left:4px solid #FF6584; padding:8px 12px; border-radius:6px; margin-bottom:10px; font-weight:700; color:#9F1239; font-size:13px;'>
            🔧 Vehicle Bus: SYNCED
        </div>
    """, unsafe_allow_html=True)

# ----------------- CONTINUOUS DATA ENGINE -----------------
if "tick" not in st.session_state:
    st.session_state.tick = 456

st.session_state.tick += 1
t = st.session_state.tick

cycle_val = st.session_state.tick
actual_soh = max(70.0, min(100.0, 99.5 - (cycle_val / 1000.0) * 15.0))
pred_soh = max(68.0, min(100.0, actual_soh + np.sin(t / 6.0) * 2.2))
pred_error = abs(actual_soh - pred_soh)

voltage = np.clip(3.9 + 0.22 * np.sin(t / 8.0) + np.random.normal(0, 0.01), 3.200, 4.200)
current = np.clip(8.5 + 14.0 * np.cos(t / 5.0) + np.random.normal(0, 0.3), -25.0, 30.0)
temp = np.clip(32.0 + (cycle_val * 0.018) + abs(current) * 0.45, 25.0, 65.0)
capacity = np.clip(3.0 * (actual_soh / 100.0), 2.100, 3.000)
resistance = np.clip(0.040 + (cycle_val / 1000.0) * 0.025, 0.035, 0.065)

# ----------------- MAIN DISPLAY -----------------
st.markdown("""
    <div class="top-header">
        <h1>🚗 EV Battery Live Monitoring & Diagnostics</h1>
        <p>Real-time vehicle telemetry stream, AI degradation estimation & thermal safety</p>
    </div>
""", unsafe_allow_html=True)

# TOP METRICS ROW
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container" style="border-top:5px solid #556B2F;"><div class="metric-sublabel">Battery Pack ID</div><div class="metric-val" style="color:#556B2F;">#01-EV</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-container" style="border-top:5px solid #38BDF8;"><div class="metric-sublabel">Cycle Count</div><div class="metric-val" style="color:#0284C7;">{cycle_val}</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-container" style="border-top:5px solid #FF6584;"><div class="metric-sublabel">Operating Temp</div><div class="metric-val" style="color:#D81B60;">{temp:.2f} °C</div></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div class="metric-container" style="border-top:5px solid #6B8E23;"><div class="metric-sublabel">Actual SOH</div><div class="metric-val" style="color:#556B2F;">{actual_soh:.2f}%</div></div>', unsafe_allow_html=True)

# SECTION: AI BATTERY HEALTH
st.markdown('<div class="section-header">⚙️ AI Battery Health Estimation</div>', unsafe_allow_html=True)

a1, a2, a3 = st.columns([1, 1, 1])

with a1:
    st.markdown(f'<div class="metric-container" style="border-left:5px solid #556B2F;"><div class="metric-sublabel">AI Predicted SOH</div><div class="metric-val" style="color:#556B2F;">{pred_soh:.2f}%</div></div>', unsafe_allow_html=True)

with a2:
    st.markdown(f'<div class="metric-container" style="border-left:5px solid #FF6584;"><div class="metric-sublabel">Model Prediction Error</div><div class="metric-val" style="color:#D81B60;">{pred_error:.2f}%</div></div>', unsafe_allow_html=True)

with a3:
    if actual_soh >= 80.0:
        st.markdown('<div class="status-badge-good">● STATUS: OPTIMAL (GOOD)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-warn">⚠️ STATUS: RETIREMENT SUGGESTED</div>', unsafe_allow_html=True)

# SECTION: ELECTRICAL PARAMETERS
st.markdown('<div class="section-header">⚡ Mechanical & Electrical Parameters</div>', unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)

with e1:
    st.markdown(f'<div class="metric-container"><div class="metric-sublabel">Terminal Voltage</div><div class="metric-val" style="color:#556B2F;">{voltage:.3f} V</div></div>', unsafe_allow_html=True)

with e2:
    st.markdown(f'<div class="metric-container"><div class="metric-sublabel">Current Load</div><div class="metric-val" style="color:#0284C7;">{current:.2f} A</div></div>', unsafe_allow_html=True)

with e3:
    st.markdown(f'<div class="metric-container"><div class="metric-sublabel">Current Capacity</div><div class="metric-val">{capacity:.3f} Ah</div></div>', unsafe_allow_html=True)

with e4:
    st.markdown(f'<div class="metric-container"><div class="metric-sublabel">Internal Resistance</div><div class="metric-val" style="color:#64748B;">{resistance:.5f} Ω</div></div>', unsafe_allow_html=True)

# Auto refresh every 1 second continuously
time.sleep(1)
st.rerun()
