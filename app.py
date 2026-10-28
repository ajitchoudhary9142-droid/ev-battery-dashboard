import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="EV Battery Live Monitoring", page_icon="🔋", layout="wide")

st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    .section-header { font-size: 20px; font-weight: 700; color: #2D3748; margin-top: 15px; margin-bottom: 12px; }
    .metric-container { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 18px; }
    .metric-sublabel { font-size: 13px; color: #718096; margin-bottom: 4px; font-weight: 500; }
    .metric-val { font-size: 26px; font-weight: 700; color: #1A202C; }
    .status-badge { display: inline-flex; align-items: center; background-color: #E6F4EA; color: #137333; font-weight: 700; font-size: 14px; padding: 6px 16px; border-radius: 20px; margin-top: 25px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔋 **EV BATTERY SYSTEM**")
    st.radio("Navigation", ["Live Dashboard", "Alerts", "History", "AI SOH", "Settings"], index=0)
    st.success("🟢 AI Model Online")
    st.success("🟢 System Online")

if "tick" not in st.session_state:
    st.session_state.tick = 456

st.session_state.tick += 1
t = st.session_state.tick

cycle_val = st.session_state.tick
actual_soh = max(70.0, min(100.0, 99.5 - (cycle_val / 1000.0) * 15.0))
pred_soh = max(68.0, min(100.0, actual_soh + np.sin(t / 5.0) * 2.5))
pred_error = abs(actual_soh - pred_soh)

voltage = np.clip(3.9 + 0.25 * np.sin(t / 8.0) + np.random.normal(0, 0.01), 3.200, 4.200)
current = np.clip(8.0 + 12.0 * np.cos(t / 6.0) + np.random.normal(0, 0.3), -25.0, 30.0)
temp = np.clip(32.0 + (cycle_val * 0.02) + abs(current) * 0.45, 25.0, 65.0)
capacity = np.clip(3.0 * (actual_soh / 100.0), 2.100, 3.000)
resistance = np.clip(0.040 + (cycle_val / 1000.0) * 0.025, 0.035, 0.065)

st.markdown("## 🔋 EV Battery Live Monitoring")
st.caption("Real-time monitoring of EV battery operating parameters")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-container"><div class="metric-sublabel">Battery ID</div><div class="metric-val">1</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-container"><div class="metric-sublabel">Cycle</div><div class="metric-val">{cycle_val}</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-container"><div class="metric-sublabel">Temperature</div><div class="metric-val">{temp:.2f} °C</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-container"><div class="metric-sublabel">Actual SOH</div><div class="metric-val">{actual_soh:.2f}%</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">⚙️ AI Battery Health</div>', unsafe_allow_html=True)
a1, a2, a3 = st.columns(3)
a1.markdown(f'<div class="metric-container"><div class="metric-sublabel">AI Predicted SOH</div><div class="metric-val">{pred_soh:.2f}%</div></div>', unsafe_allow_html=True)
a2.markdown(f'<div class="metric-container"><div class="metric-sublabel">Prediction Error</div><div class="metric-val">{pred_error:.2f}%</div></div>', unsafe_allow_html=True)
a3.markdown('<div class="status-badge">● GOOD</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">⚡ Electrical Parameters</div>', unsafe_allow_html=True)
e1, e2, e3, e4 = st.columns(4)
e1.markdown(f'<div class="metric-container"><div class="metric-sublabel">Voltage</div><div class="metric-val">{voltage:.3f} V</div></div>', unsafe_allow_html=True)
e2.markdown(f'<div class="metric-container"><div class="metric-sublabel">Current</div><div class="metric-val">{current:.2f} A</div></div>', unsafe_allow_html=True)
e3.markdown(f'<div class="metric-container"><div class="metric-sublabel">Capacity</div><div class="metric-val">{capacity:.3f} Ah</div></div>', unsafe_allow_html=True)
e4.markdown(f'<div class="metric-container"><div class="metric-sublabel">Resistance</div><div class="metric-val">{resistance:.5f} Ω</div></div>', unsafe_allow_html=True)

time.sleep(1)
st.rerun()
