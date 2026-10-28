import streamlit as st
import numpy as np
import time
import base64
import os

st.set_page_config(
    page_title="EV Cockpit & Telemetry HUD",
    page_icon="🏎️",
    layout="wide"
)

# Function to load local image as base64 background
def get_base64_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

bg_base64 = get_base64_bg("car_bg.jpg")

# 100% ORIGINAL IMAGE (NO FADED WHITE OVERLAY)
if bg_base64:
    bg_style = f"""
        background: url('data:image/jpeg;base64,{bg_base64}') no-repeat center center fixed !important;
    """
else:
    bg_style = """
        background: url('https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed !important;
    """

st.markdown(f"""
<style>
    /* Full original HD background */
    .stApp {{
        {bg_style}
        background-size: cover !important;
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif !important;
        color: #FAFAFA !important;
    }}

    .bolt {{
        position: absolute;
        width: 8px;
        height: 8px;
        background: radial-gradient(circle, #CBD5E1 40%, #64748B 90%);
        border-radius: 50%;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    .b-tl {{ top: 6px; left: 6px; }}
    .b-tr {{ top: 6px; right: 6px; }}
    .b-bl {{ bottom: 6px; left: 6px; }}
    .b-br {{ bottom: 6px; right: 6px; }}

    /* 1. SOLID VIBRANT OLIVE GREEN HEXAGON */
    .shape-olive-hex {{
        position: relative;
        background: linear-gradient(145deg, rgba(85, 107, 47, 0.95), rgba(50, 65, 25, 0.95));
        color: #FAFAFA !important;
        padding: 22px 18px;
        clip-path: polygon(15px 0%, 100% 0%, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0% 100%, 0% 15px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        border: 2px solid #84A346;
        backdrop-filter: blur(4px);
    }}

    /* 2. SOLID VIBRANT LIGHT PINK CAPSULE */
    .shape-pink-pill {{
        position: relative;
        background: linear-gradient(145deg, rgba(255, 228, 232, 0.95), rgba(255, 182, 193, 0.95));
        color: #881337 !important;
        padding: 22px 20px;
        border-radius: 35px 8px 35px 8px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        border: 2px solid #FF6584;
        backdrop-filter: blur(4px);
    }}

    /* 3. SOLID VIBRANT SKY BLUE QUAD */
    .shape-blue-quad {{
        position: relative;
        background: linear-gradient(145deg, rgba(2, 132, 199, 0.95), rgba(14, 165, 233, 0.95));
        color: #FAFAFA !important;
        padding: 22px 18px;
        border-radius: 8px 30px 8px 30px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        border: 2px solid #38BDF8;
        backdrop-filter: blur(4px);
    }}

    /* 4. SOLID FAIR WHITE INDUSTRIAL CASING */
    .shape-white-case {{
        position: relative;
        background: rgba(250, 250, 250, 0.95);
        color: #1E293B !important;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #E2E8F0;
        border-left: 7px solid #556B2F;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
    }}

    .hud-title {{
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
        opacity: 0.95;
    }}

    .hud-val {{
        font-size: 32px;
        font-weight: 900;
        font-family: 'Impact', 'Arial Black', sans-serif;
        letter-spacing: 0.5px;
    }}

    /* Top Cockpit Header */
    .cockpit-banner {{
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 50%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid #38BDF8;
        border-top: 5px solid #556B2F;
        color: #FAFAFA;
        padding: 16px 24px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.7);
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(6px);
    }}
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#556B2F; margin:0;'>🏎️ PIT-STOP CONSOLE</h2>", unsafe_allow_html=True)
    st.caption("Vehicle ECU Diagnostic Terminal")
    st.markdown("---")
    
    st.markdown("<b>🛠️ Mechanical Adjustments</b>", unsafe_allow_html=True)
    aging_sim = st.slider("Simulated Pack Mileage (Cycles)", 100, 1200, 456, step=25)
    speed_rate = st.slider("ECU Refresh Rate (Sec)", 1, 3, 1)
    
    st.markdown("---")
    st.markdown("""
        <div style='background:#556B2F; color:#FFF; padding:10px; border-radius:8px; font-weight:700; font-size:12px; margin-bottom:10px; text-align:center;'>
            ⚙️ POWERTRAIN: LINKED
        </div>
        <div style='background:#0284C7; color:#FFF; padding:10px; border-radius:8px; font-weight:700; font-size:12px; margin-bottom:10px; text-align:center;'>
            🔋 EV CHARGER: CONNECTED
        </div>
        <div style='background:#FFE4E8; color:#9F1239; border:1px solid #FF6584; padding:10px; border-radius:8px; font-weight:700; font-size:12px; text-align:center;'>
            🔧 THERMAL CHOPPER: READY
        </div>
    """, unsafe_allow_html=True)

# ----------------- CONTINUOUS TELEMETRY -----------------
if "tick" not in st.session_state:
    st.session_state.tick = aging_sim

st.session_state.tick += 1
t = st.session_state.tick

cycle_val = st.session_state.tick
actual_soh = max(70.0, min(100.0, 99.5 - (cycle_val / 1000.0) * 15.0))
pred_soh = max(68.0, min(100.0, actual_soh + np.sin(t / 4.0) * 2.1))
pred_error = abs(actual_soh - pred_soh)

voltage = np.clip(3.9 + 0.22 * np.sin(t / 6.0) + np.random.normal(0, 0.01), 3.200, 4.200)
current = np.clip(8.5 + 13.5 * np.cos(t / 5.0) + np.random.normal(0, 0.2), -25.0, 30.0)
temp = np.clip(31.5 + (cycle_val * 0.018) + abs(current) * 0.42, 25.0, 65.0)
capacity = np.clip(3.0 * (actual_soh / 100.0), 2.100, 3.000)
resistance = np.clip(0.040 + (cycle_val / 1000.0) * 0.024, 0.035, 0.065)

# ----------------- TOP BANNER -----------------
st.markdown(f"""
    <div class="cockpit-banner">
        <div>
            <div style="font-size:11px; letter-spacing:2px; color:#38BDF8; font-weight:800;">DIAGNOSTIC TELEMETRY CLUSTER</div>
            <h1 style="margin:2px 0 0 0; font-size:24px; color:#FAFAFA; font-weight:900;">🏎️ EV BATTERY LIVE MONITORING CONSOLE</h1>
        </div>
        <div style="text-align:right;">
            <div style="background:#556B2F; color:#FFF; font-weight:800; padding:6px 16px; border-radius:20px; font-size:12px; display:inline-block; border:1px solid #84A346;">
                ● LIVE CHARGING / CAN-BUS
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------- METRIC CARDS -----------------
r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown("""
        <div class="shape-olive-hex">
            <div class="bolt b-tr"></div>
            <div class="bolt b-bl"></div>
            <div class="hud-title">CHASSIS PACK ID</div>
            <div class="hud-val">#01-EV</div>
            <div style="font-size:11px; opacity:0.9; margin-top:4px;">LITHIUM-ION MODULE</div>
        </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
        <div class="shape-blue-quad">
            <div class="bolt b-tl"></div>
            <div class="bolt b-br"></div>
            <div class="hud-title">MILEAGE CYCLES</div>
            <div class="hud-val">{cycle_val}</div>
            <div style="font-size:11px; opacity:0.9; margin-top:4px;">TOTAL DRIVE CYCLES</div>
        </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
        <div class="shape-pink-pill">
            <div class="bolt b-tr"></div>
            <div class="bolt b-bl"></div>
            <div class="hud-title" style="color:#881337;">CELL TEMPERATURE</div>
            <div class="hud-val" style="color:#881337;">{temp:.2f} °C</div>
            <div style="font-size:11px; opacity:0.9; margin-top:4px; color:#881337;">CORE THERMAL SENSOR</div>
        </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown(f"""
        <div class="shape-olive-hex">
            <div class="bolt b-tl"></div>
            <div class="bolt b-br"></div>
            <div class="hud-title">ACTUAL SOH (HEALTH)</div>
            <div class="hud-val">{actual_soh:.2f}%</div>
            <div style="font-size:11px; opacity:0.9; margin-top:4px;">CAPACITY RETENTION</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- AI HEALTH SECTION -----------------
st.markdown("<h3 style='color:#38BDF8; font-size:18px; font-weight:800; letter-spacing:1px; text-shadow:0 2px 4px #000;'>⚙️ AI DIAGNOSTIC & HEALTH CLUSTER</h3>", unsafe_allow_html=True)

a1, a2, a3 = st.columns([1, 1, 1.2])

with a1:
    st.markdown(f"""
        <div class="shape-white-case" style="border-left:7px solid #556B2F;">
            <div class="bolt b-tr"></div>
            <div class="hud-title" style="color:#556B2F;">AI PREDICTED SOH</div>
            <div class="hud-val" style="color:#556B2F;">{pred_soh:.2f}%</div>
            <div style="font-size:12px; color:#64748B; margin-top:4px;">Deep Neural Net Inference</div>
        </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown(f"""
        <div class="shape-pink-pill" style="border-radius:12px;">
            <div class="bolt b-tl"></div>
            <div class="hud-title" style="color:#881337;">PREDICTION ERROR</div>
            <div class="hud-val" style="color:#881337;">{pred_error:.2f}%</div>
            <div style="font-size:12px; opacity:0.9; margin-top:4px; color:#881337;">Dynamic Residual Drift</div>
        </div>
    """, unsafe_allow_html=True)

with a3:
    status_color = "#556B2F" if actual_soh >= 80.0 else "#E11D48"
    status_text = "OPTIMAL (PASS)" if actual_soh >= 80.0 else "REPLACE REQUIRED"
    st.markdown(f"""
        <div class="shape-white-case" style="border-left:7px solid #0284C7; text-align:center; padding:18px;">
            <div class="hud-title" style="color:#0284C7;">BATTERY PACK STATUS VERDICT</div>
            <div style="background:{status_color}; color:#FFF; font-weight:900; font-size:18px; padding:8px 24px; border-radius:30px; display:inline-block; margin-top:6px; box-shadow:0 4px 10px rgba(0,0,0,0.3);">
                ● {status_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- ELECTRICAL TELEMETRY -----------------
st.markdown("<h3 style='color:#38BDF8; font-size:18px; font-weight:800; letter-spacing:1px; text-shadow:0 2px 4px #000;'>⚡ POWERTRAIN ELECTRICAL TELEMETRY</h3>", unsafe_allow_html=True)

e1, e2, e3, e4 = st.columns(4)

with e1:
    st.markdown(f"""
        <div class="shape-white-case" style="border-left:6px solid #556B2F;">
            <div class="hud-title" style="color:#556B2F;">TERMINAL VOLTAGE</div>
            <div class="hud-val" style="color:#556B2F;">{voltage:.3f} V</div>
            <div style="font-size:11px; color:#64748B;">BUS VOLTAGE [3.2 - 4.2V]</div>
        </div>
    """, unsafe_allow_html=True)

with e2:
    st.markdown(f"""
        <div class="shape-blue-quad">
            <div class="bolt b-bl"></div>
            <div class="hud-title">CURRENT DRAW</div>
            <div class="hud-val">{current:.2f} A</div>
            <div style="font-size:11px; opacity:0.9;">CHARGING / DRIVE LOAD</div>
        </div>
    """, unsafe_allow_html=True)

with e3:
    st.markdown(f"""
        <div class="shape-white-case" style="border-left:6px solid #0284C7;">
            <div class="hud-title" style="color:#0284C7;">USABLE CAPACITY</div>
            <div class="hud-val" style="color:#0284C7;">{capacity:.3f} Ah</div>
            <div style="font-size:11px; color:#64748B;">NOMINAL: 3.000 Ah</div>
        </div>
    """, unsafe_allow_html=True)

with e4:
    st.markdown(f"""
        <div class="shape-white-case" style="border-left:6px solid #64748B;">
            <div class="hud-title" style="color:#64748B;">INTERNAL IMPEDANCE (R₀)</div>
            <div class="hud-val" style="color:#1E293B;">{resistance:.5f} Ω</div>
            <div style="font-size:11px; color:#64748B;">CELL RESISTANCE</div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(speed_rate)
st.rerun()
