import streamlit as st
import numpy as np
import time

st.set_page_config(
    page_title="EV Battery Live Monitoring Console",
    page_icon="🚗",
    layout="wide"
)

# ----------------- CUSTOM INTERACTIVE CSS (FAIR WHITE BASE + FILLED COLORED BOXES) -----------------
st.markdown("""
<style>
    /* 1. Fair White Base with Mechanical Vehicle Workshop Watermark */
    .stApp {
        background-color: #FAFAFA;
        background-image: 
            linear-gradient(rgba(250, 250, 250, 0.92), rgba(250, 250, 250, 0.94)),
            url('https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1A202C;
    }

    /* 2. Filled Olive Green Mechanical Box (Chamfered Top-Right Corner) */
    .box-olive {
        background: linear-gradient(135deg, #556B2F, #435424);
        color: #FAFAFA;
        padding: 18px 20px;
        border-radius: 8px 24px 8px 8px;
        box-shadow: 0 6px 14px rgba(85, 107, 47, 0.28);
        border: 2px solid #6B8E23;
        transition: transform 0.2s ease;
    }
    .box-olive:hover { transform: translateY(-3px); }

    /* 3. Filled Sky Blue Box (Chamfered Top-Left Corner) */
    .box-skyblue {
        background: linear-gradient(135deg, #0284C7, #0369A1);
        color: #FAFAFA;
        padding: 18px 20px;
        border-radius: 24px 8px 8px 8px;
        box-shadow: 0 6px 14px rgba(2, 132, 199, 0.28);
        border: 2px solid #38BDF8;
        transition: transform 0.2s ease;
    }
    .box-skyblue:hover { transform: translateY(-3px); }

    /* 4. Filled Light Pink Box (Hexagonal Cut Corners) */
    .box-lightpink {
        background: linear-gradient(135deg, #FFE4E8, #FFD1D9);
        color: #9F1239;
        padding: 18px 20px;
        border-radius: 12px;
        clip-path: polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px);
        box-shadow: 0 6px 14px rgba(255, 182, 193, 0.45);
        border: 2px solid #F8B4C0;
        transition: transform 0.2s ease;
    }
    .box-lightpink:hover { transform: translateY(-3px); }

    /* 5. Pure Fair White Mechanical Box with Rivet Accents */
    .box-fairwhite {
        background-color: #FFFFFF;
        color: #2D3748;
        padding: 18px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 2px solid #E2E8F0;
        border-top: 5px solid #556B2F;
        transition: transform 0.2s ease;
    }
    .box-fairwhite:hover { transform: translateY(-3px); }

    /* Card Text Styling */
    .label-light {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        opacity: 0.88;
        margin-bottom: 6px;
    }
    .val-large {
        font-size: 28px;
        font-weight: 800;
        font-family: 'Consolas', monospace;
    }

    /* Section Subheadings */
    .mech-heading {
        color: #2D3748;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 25px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Status Capsule */
    .capsule-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 13px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR INTERACTIVE TOOLS -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#556B2F; margin:0;'>🚗 EV CHASSIS RIG</h2>", unsafe_allow_html=True)
    st.caption("Industrial Diagnostics Panel")
    
    st.markdown("---")
    st.markdown("<b>⚙️ Telemetry Controls</b>", unsafe_allow_html=True)
    sim_speed = st.slider("Update Rate (Seconds)", min_value=1, max_value=3, value=1)
    cycle_jump = st.slider("Simulate Aging Step (Cycles)", min_value=1, max_value=20, value=2)
    
    st.markdown("---")
    st.markdown("""
        <div style='background:#556B2F; color:#FAFAFA; padding:8px 14px; border-radius:6px; margin-bottom:8px; font-weight:700; font-size:12px;'>
            🟢 CAN-BUS: SYNCHRONIZED
        </div>
        <div style='background:#0284C7; color:#FAFAFA; padding:8px 14px; border-radius:6px; margin-bottom:8px; font-weight:700; font-size:12px;'>
            🔵 BMS INVERTER: ACTIVE
        </div>
        <div style='background:#FFE4E8; color:#9F1239; border:1px solid #F8B4C0; padding:8px 14px; border-radius:6px; font-weight:700; font-size:12px;'>
            🔧 THERMAL CHOPPER: ONLINE
        </div>
    """, unsafe_allow_html=True)

# ----------------- CONTINUOUS TELEMETRY TICK ENGINE -----------------
if "tick" not in st.session_state:
    st.session_state.tick = 456

st.session_state.tick += cycle_jump
t = st.session_state.tick

cycle_val = st.session_state.tick
actual_soh = max(70.0, min(100.0, 99.5 - (cycle_val / 1000.0) * 15.0))
pred_soh = max(68.0, min(100.0, actual_soh + np.sin(t / 5.0) * 2.3))
pred_error = abs(actual_soh - pred_soh)

voltage = np.clip(3.9 + 0.22 * np.sin(t / 7.0) + np.random.normal(0, 0.01), 3.200, 4.200)
current = np.clip(8.5 + 13.0 * np.cos(t / 5.0) + np.random.normal(0, 0.25), -25.0, 30.0)
temp = np.clip(32.0 + (cycle_val * 0.016) + abs(current) * 0.42, 25.0, 65.0)
capacity = np.clip(3.0 * (actual_soh / 100.0), 2.100, 3.000)
resistance = np.clip(0.040 + (cycle_val / 1000.0) * 0.024, 0.035, 0.065)

# ----------------- HEADER BANNER (FAIR WHITE + OLIVE ACCENT) -----------------
st.markdown("""
    <div style='background:#FFFFFF; border:2px solid #E2E8F0; border-left:8px solid #556B2F; border-radius:12px; padding:18px 24px; box-shadow:0 4px 14px rgba(0,0,0,0.05); margin-bottom:20px;'>
        <h1 style='margin:0; font-size:26px; color:#556B2F; font-weight:800; letter-spacing:0.5px;'>
            🚗 EV Battery Live Monitoring Console
        </h1>
        <p style='margin:5px 0 0 0; color:#718096; font-size:14px; font-weight:600;'>
            Vehicle Chassis Telemetry & Mechanical Battery Pack SOH Diagnostic System
        </p>
    </div>
""", unsafe_allow_html=True)

# ----------------- ROW 1: PRIMARY METRICS IN DIFFERENT FILLED SHAPES -----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
        <div class="box-olive">
            <div class="label-light">PACK IDENTIFIER</div>
            <div class="val-large">#01-EV</div>
            <div style="font-size:12px; opacity:0.8; margin-top:4px;">Chassis Pack Unit</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="box-skyblue">
            <div class="label-light">CYCLIC AGING</div>
            <div class="val-large">{cycle_val}</div>
            <div style="font-size:12px; opacity:0.8; margin-top:4px;">Charge / Discharge Cycles</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="box-lightpink">
            <div class="label-light" style="color:#9F1239;">PACK CORE TEMPERATURE</div>
            <div class="val-large" style="color:#9F1239;">{temp:.2f} °C</div>
            <div style="font-size:12px; opacity:0.8; margin-top:4px; color:#9F1239;">Joule Thermal Load</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class="box-olive">
            <div class="label-light">ACTUAL SOH (HEALTH)</div>
            <div class="val-large">{actual_soh:.2f}%</div>
            <div style="font-size:12px; opacity:0.8; margin-top:4px;">Degradation Capacity Factor</div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- SECTION: AI BATTERY HEALTH (FILLED MECHANICAL BOXES) -----------------
st.markdown('<div class="mech-heading">⚙️ AI Battery Health Intelligence</div>', unsafe_allow_html=True)

a1, a2, a3 = st.columns(3)

with a1:
    st.markdown(f"""
        <div class="box-fairwhite" style="border-top:5px solid #556B2F;">
            <div class="label-light" style="color:#556B2F;">AI PREDICTED SOH</div>
            <div class="val-large" style="color:#556B2F;">{pred_soh:.2f}%</div>
            <div style="font-size:12px; color:#718096; margin-top:4px;">Machine Learning Inference</div>
        </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown(f"""
        <div class="box-lightpink">
            <div class="label-light" style="color:#9F1239;">PREDICTION DEVIATION ERROR</div>
            <div class="val-large" style="color:#9F1239;">{pred_error:.2f}%</div>
            <div style="font-size:12px; opacity:0.8; margin-top:4px; color:#9F1239;">Residual Dynamic Error</div>
        </div>
    """, unsafe_allow_html=True)

with a3:
    if actual_soh >= 80.0:
        badge_html = '<span class="capsule-badge" style="background:#556B2F; color:#FAFAFA;">● STATUS: GOOD (OPTIMAL)</span>'
    else:
        badge_html = '<span class="capsule-badge" style="background:#FFE4E8; border:1.5px solid #FF6584; color:#9F1239;">⚠️ STATUS: RETIREMENT LIMIT</span>'
    
    st.markdown(f"""
        <div class="box-fairwhite" style="border-top:5px solid #0284C7; text-align:center; padding-top:24px;">
            <div class="label-light" style="color:#0284C7;">SYSTEM VERDICT</div>
            <div style="margin-top:10px;">{badge_html}</div>
        </div>
    """, unsafe_allow_html=True)

# ----------------- SECTION: ELECTRICAL PARAMETERS (SHAPED FILLED BOXES) -----------------
st.markdown('<div class="mech-heading">⚡ Real-Time Electrical Telemetry</div>', unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)

with e1:
    st.markdown(f"""
        <div class="box-fairwhite" style="border-left:6px solid #556B2F;">
            <div class="label-light" style="color:#556B2F;">TERMINAL VOLTAGE</div>
            <div class="val-large" style="color:#556B2F;">{voltage:.3f} V</div>
            <div style="font-size:12px; color:#718096; margin-top:4px;">Bus Potential</div>
        </div>
    """, unsafe_allow_html=True)

with e2:
    st.markdown(f"""
        <div class="box-skyblue">
            <div class="label-light">CURRENT FLOW (DRAW)</div>
            <div class="val-large">{current:.2f} A</div>
            <div style="font-size:12px; opacity:0.8; margin-top:4px;">Active Drive Cycle Load</div>
        </div>
    """, unsafe_allow_html=True)

with e3:
    st.markdown(f"""
        <div class="box-fairwhite" style="border-left:6px solid #0284C7;">
            <div class="label-light" style="color:#0284C7;">ACTIVE PACK CAPACITY</div>
            <div class="val-large" style="color:#0284C7;">{capacity:.3f} Ah</div>
            <div style="font-size:12px; color:#718096; margin-top:4px;">Coulomb Charge Total</div>
        </div>
    """, unsafe_allow_html=True)

with e4:
    st.markdown(f"""
        <div class="box-fairwhite" style="border-left:6px solid #64748B;">
            <div class="label-light" style="color:#64748B;">INTERNAL RESISTANCE (R₀)</div>
            <div class="val-large" style="color:#1E293B;">{resistance:.5f} Ω</div>
            <div style="font-size:12px; color:#718096; margin-top:4px;">Ohmic Degradation</div>
        </div>
    """, unsafe_allow_html=True)

# Continuous smooth loop execution
time.sleep(sim_speed)
st.rerun()
