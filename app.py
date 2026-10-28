import streamlit as st
import numpy as np
import time

st.set_page_config(
    page_title="EV Cockpit & Telemetry HUD",
    page_icon="🏎️",
    layout="wide"
)

# ----------------- MECHANICAL COCKPIT THEME (FAIR WHITE BASE + EV FUTURISTIC CAR BG) -----------------
st.markdown("""
<style>
    /* Futuristic EV Charging Car Background with Fair White Overlay */
    .stApp {
        background: 
            linear-gradient(rgba(250, 250, 250, 0.88), rgba(250, 250, 250, 0.93)),
            url('https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=1920&q=80') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif !important;
        color: #1A202C !important;
    }

    /* Bolt / Rivet for Mechanical Realism */
    .bolt {
        position: absolute;
        width: 8px;
        height: 8px;
        background: radial-gradient(circle, #CBD5E1 40%, #64748B 90%);
        border-radius: 50%;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.25);
    }
    .b-tl { top: 6px; left: 6px; }
    .b-tr { top: 6px; right: 6px; }
    .b-bl { bottom: 6px; left: 6px; }
    .b-br { bottom: 6px; right: 6px; }

    /* 1. SOLID FILLED OLIVE GREEN HEXAGONAL BOX */
    .shape-olive-hex {
        position: relative;
        background: linear-gradient(145deg, #556B2F, #425424);
        color: #FFFFFF !important;
        padding: 22px 18px;
        clip-path: polygon(15px 0%, 100% 0%, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0% 100%, 0% 15px);
        box-shadow: 0 10px 20px rgba(85, 107, 47, 0.35);
        border: 2px solid #6B8E23;
        transition: 0.3s;
    }
    .shape-olive-hex:hover { transform: scale(1.02); }

    /* 2. SOLID FILLED LIGHT PINK ROUNDED CAPSULE BOX */
    .shape-pink-pill {
        position: relative;
        background: linear-gradient(145deg, #FFE4E8, #FFC0CB);
        color: #881337 !important;
        padding: 22px 20px;
        border-radius: 35px 8px 35px 8px;
        box-shadow: 0 10px 20px rgba(255, 182, 193, 0.45);
        border: 2px solid #FB7185;
        transition: 0.3s;
    }
    .shape-pink-pill:hover { transform: scale(1.02); }

    /* 3. SOLID FILLED SKY BLUE BEVELED QUAD BOX */
    .shape-blue-quad {
        position: relative;
        background: linear-gradient(145deg, #0284C7, #0369A1);
        color: #FFFFFF !important;
        padding: 22px 18px;
        border-radius: 8px 30px 8px 30px;
        box-shadow: 0 10px 20px rgba(2, 132, 199, 0.35);
        border: 2px solid #38BDF8;
        transition: 0.3s;
    }
    .shape-blue-quad:hover { transform: scale(1.02); }

    /* 4. SOLID FAIR WHITE INDUSTRIAL MACHINED CASING */
    .shape-white-case {
        position: relative;
        background: #FFFFFF;
        color: #1E293B !important;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #E2E8F0;
        border-left: 6px solid #556B2F;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }

    .hud-title {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
        opacity: 0.9;
    }

    .hud-val {
        font-size: 32px;
        font-weight: 900;
        font-family: 'Impact', 'Arial Black', sans-serif;
        letter-spacing: 0.5px;
    }

    /* Top Cockpit Instrument Banner */
    .cockpit-banner {
        background: linear-gradient(90deg, #1E293B 0%, #334155 50%, #1E293B 100%);
        border: 3px solid #64748B;
        border-top: 5px solid #556B2F;
        color: #FAFAFA;
        padding: 16px 24px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: CAR WORKSHOP CONTROLS -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#556B2F; margin:0;'>🏎️ TELEMETRY PIT-STOP</h2>", unsafe_allow_html=True)
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
        <div style='background:#38BDF8; color:#0369A1; padding:10px; border-radius:8px; font-weight:700; font-size:12px; margin-bottom:10px; text-align:center;'>
            🔋 EV CHARGER: CONNECTED
        </div>
        <div style='background:#FFE4E8; color:#9F1239; border:1px solid #FB7185; padding:10px; border-radius:8px; font-weight:700; font-size:12px; text-align:center;'>
            🔧 THERMAL CHOPPER: READY
        </div>
    """, unsafe_allow_html=True)

# ----------------- CONTINUOUS DATA SYNTHESIS -----------------
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

# ----------------- TOP VEHICLE COCKPIT BANNER -----------------
st.markdown(f"""
    <div class="cockpit-banner">
        <div>
            <div style="font-size:11px; letter-spacing:2px; color:#38BDF8; font-weight:800;">DIAGNOSTIC TELEMETRY CLUSTER</div>
            <h1 style="margin:2px 0 0 0; font-size:24px; color:#FAFAFA; font-weight:900;">🏎️ EV BATTERY LIVE MONITORING CONSOLE</h1>
        </div>
        <div style="text-align:right;">
            <div style="background:#556B2F; color:#FFF; font-weight:800; padding:6px 16px; border-radius:20px; font-size:12px; display:inline-block;">
                ● LIVE CHARGING / CAN-BUS FEED
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------- ROW 1: PRIMARY METRICS IN DIFFERENT FILLED SHAPES -----------------
r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown("""
        <div class="shape-olive-hex">
            <div class="bolt b-tr"></div>
            <div class="bolt b-bl"></div>
            <div class="hud-title">CHASSIS PACK ID</div>
            <div class="hud-val">#01-EV</div>
            <div style="font-size:11px; opacity:0.85; margin-top:4px;">LITHIUM-ION MODULE</div>
        </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
        <div class="shape-blue-quad">
            <div class="bolt b-tl"></div>
            <div class="bolt b-br"></div>
            <div class="hud-title">MILEAGE CYCLES</div>
            <div class="hud-val">{cycle_val}</div>
            <div style="font-size:11px; opacity:0.85; margin-top:4px;">TOTAL DRIVE CYCLES</div>
        </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
        <div class="shape-pink-pill">
            <div class="bolt b-tr"></div>
            <div class="bolt b-bl"></div>
            <div class="hud-title" style="color:#881337;">CELL TEMPERATURE</div>
            <div class="hud-val" style="color:#881337;">{temp:.2f} °C</div>
            <div style="font-size:11px; opacity:0.85; margin-top:4px; color:#881337;">CORE THERMAL SENSOR</div>
        </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown(f"""
        <div class="shape-olive-hex">
            <div class="bolt b-tl"></div>
            <div class="bolt b-br"></div>
            <div class="hud-title">ACTUAL SOH (HEALTH)</div>
            <div class="hud-val">{actual_soh:.2f}%</div>
            <div style="font-size:11px; opacity:0.85; margin-top:4px;">CAPACITY RETENTION</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- SECTION 2: AI BATTERY HEALTH -----------------
st.markdown("<h3 style='color:#556B2F; font-size:18px; font-weight:800; letter-spacing:1px;'>⚙️ AI DIAGNOSTIC & HEALTH CLUSTER</h3>", unsafe_allow_html=True)

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
            <div style="font-size:12px; opacity:0.85; margin-top:4px; color:#881337;">Dynamic Residual Drift</div>
        </div>
    """, unsafe_allow_html=True)

with a3:
    status_color = "#556B2F" if actual_soh >= 80.0 else "#E11D48"
    status_text = "OPTIMAL (PASS)" if actual_soh >= 80.0 else "REPLACE REQUIRED"
    st.markdown(f"""
        <div class="shape-white-case" style="border-left:7px solid #0284C7; text-align:center; padding:18px;">
            <div class="hud-title" style="color:#0284C7;">BATTERY PACK STATUS VERDICT</div>
            <div style="background:{status_color}; color:#FFF; font-weight:900; font-size:18px; padding:8px 24px; border-radius:30px; display:inline-block; margin-top:6px; box-shadow:0 4px 10px rgba(0,0,0,0.15);">
                ● {status_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- SECTION 3: ELECTRICAL TELEMETRY -----------------
st.markdown("<h3 style='color:#0284C7; font-size:18px; font-weight:800; letter-spacing:1px;'>⚡ POWERTRAIN ELECTRICAL TELEMETRY</h3>", unsafe_allow_html=True)

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
            <div style="font-size:11px; opacity:0.85;">CHARGING / DRIVE LOAD</div>
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

# Auto Refresh loop
time.sleep(speed_rate)
st.rerun()
