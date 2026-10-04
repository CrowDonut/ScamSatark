"""
app.py - ScamSatark Main Application Entry Point
Investor Resilience Platform for SANGYAN Hackathon (SEBI / NSDL / IIT BHU)
"""
import os
import streamlit as st
from PIL import Image, ImageDraw
from dotenv import load_dotenv

# Import modular team components
from ui_components import inject_custom_styles, render_hero, render_risk_gauge, render_actionable_redressal
from ai_scanner import analyze_image_for_scams
from voice_engine import generate_regional_audio
from sebi_rules import audit_sebi_compliance
from database import init_db, log_scan, get_radar_analytics

# Initialize system
load_dotenv()
init_db()

st.set_page_config(
    page_title="ScamSatark | SEBI Investor Resilience",
    page_icon="🛡️",
    layout="centered"
)
inject_custom_styles()
render_hero()

# Sidebar: Language & Configuration
st.sidebar.header("🌐 Language / भाषा")
selected_lang = st.sidebar.selectbox("Choose Language", ["हिन्दी (Hindi)", "English", "தமிழ் (Tamil)"])

st.sidebar.markdown("---")
st.sidebar.header("🔑 Credentials")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Built-in Sample Generator for Quick Judge Testing
st.sidebar.markdown("---")
st.sidebar.header("🧪 Instant Demo Scenarios")
st.sidebar.caption("Click below to test without uploading a file:")
sample_choice = st.sidebar.radio(
    "Select a Scenario:",
    ["None (Upload Custom Image)", "Sample 1: Telegram VIP 200% Profit Scam", "Sample 2: Fake SEBI Adviser Letter", "Sample 3: Legitimate Statutory Notice"]
)

def create_sample_image(scenario_type: str) -> Image.Image:
    """Dynamically generates test scam images with visible fraudulent text."""
    img = Image.new("RGB", (650, 320), color="#1E293B")
    draw = ImageDraw.Draw(img)
    
    if "Sample 1" in scenario_type:
        text = "⚡ VIP INTRADAY SIGNALS ⚡\nJoin VIP Group! Guaranteed 200% profit daily.\nDeposit Rs. 10,000 on UPI: trader_raj@okaxis\nSEBI Reg No: SEBI/VIP/2026/PRO\nOnly 3 slots remaining! Send screenshot."
        draw.text((25, 30), text, fill="#F87171")
    elif "Sample 2" in scenario_type:
        text = "GOVERNMENT OF INDIA - FINANCIAL RECOVERY\nDear Investor, your blocked trading funds of Rs 85,000\ncan be recovered under SEBI Guaranteed Recovery.\nPay release fee of Rs 3,500 to Admin Account.\nSEBI Clearance Reg: INA999999999-VIP"
        draw.text((25, 30), text, fill="#FBBF24")
    else:
        text = "ABC SECURITIES PVT LTD (SEBI Reg: INZ000123456)\nStatutory Investor Advisory:\nInvestments in securities market are subject to market risks.\nRead all scheme related documents carefully before investing.\nNever share your trading passwords or OTPs."
        draw.text((25, 30), text, fill="#34D399")
        
    return img

# Application Tabs
tab_scan, tab_radar, tab_rules = st.tabs(["📸 Scam & Claim Scanner", "📊 Community Scam Radar", "📜 SEBI Investor Playbook"])

# TAB 1: SCANNER
with tab_scan:
    st.write("Upload a screenshot from Telegram, WhatsApp, or Instagram to verify legitimacy:")
    
    uploaded_file = st.file_uploader("Drop image here...", type=["png", "jpg", "jpeg"])
    active_image = None
    
    if sample_choice != "None (Upload Custom Image)":
        active_image = create_sample_image(sample_choice)
        st.info(f"Loaded **{sample_choice}** for evaluation:")
        st.image(active_image, caption="Simulated Evidence", use_container_width=True)
    elif uploaded_file:
        active_image = Image.open(uploaded_file)
        st.image(active_image, caption="Uploaded Evidence", use_container_width=True)

    if active_image and st.button("🔍 Check Scam Risk (जोखिम जांचें)", type="primary", use_container_width=True):
        with st.spinner("Analyzing deceptive patterns and checking SEBI regulatory rules..."):
            try:
                # 1. AI Vision Analysis (Gayatri)
                ai_res = analyze_image_for_scams(active_image, selected_lang, api_key)
                
                # 2. SEBI Regulatory Compliance Check (Pranav)
                sebi_audit = audit_sebi_compliance(ai_res.get("raw_text", ""))
                
                # 3. Blended Composite Risk Score
                final_score = min(100, max(ai_res.get("ai_risk_score", 0), sebi_audit.get("regulatory_penalty", 0)))
                final_level = "HIGH" if final_score >= 70 else ("MODERATE" if final_score >= 40 else "LOW")
                
                # 4. Log Telemetry to Database (Aryan)
                primary_flag = (ai_res.get("red_flags") or sebi_audit.get("violations") or ["Unverified content"])[0]
                log_scan(
                    platform="Telegram/WhatsApp",
                    risk_score=final_score,
                    risk_level=final_level,
                    primary_flag=primary_flag,
                    language=selected_lang
                )
                
                # 5. Render Visual Results (Saina)
                render_risk_gauge(
                    final_score=final_score,
                    level=final_level,
                    confidence=ai_res.get("confidence_score", 85),
                    rationale=ai_res.get("uncertainty_rationale", "Standard visual inspection")
                )
                
                # Display Detected Red Flags
                st.subheader("🚩 Detected Deceptive Vectors & Regulatory Breaches:")
                combined_flags = list(set(ai_res.get("red_flags", []) + sebi_audit.get("violations", [])))
                for flag in combined_flags:
                    st.markdown(f"- ⚠️ **{flag}**")
                    
                # SEBI Registration Status
                reg_status = sebi_audit.get("registration_status", {})
                if reg_status.get("found"):
                    if reg_status.get("is_valid_format"):
                        st.success(f"Verified SEBI Registration Format: `{reg_status['raw_string']}` ({reg_status['category']})")
                    else:
                        st.error(f"Invalid / Fabricated SEBI Registration Claim: `{reg_status['raw_string']}`")
                        
                # Regional Voice Output (Gayatri)
                st.markdown("---")
                st.subheader("🔊 Regional Audio Explanation (Bharat-First):")
                explanation_text = ai_res.get("plain_explanation_regional") or ai_res.get("plain_explanation_english", "")
                st.info(f"🗣️ *\"{explanation_text}\"*")
                
                audio_path = generate_regional_audio(explanation_text, selected_lang)
                if audio_path and os.path.exists(audio_path):
                    st.audio(audio_path, format="audio/mp3")
                    
                # 1-Click Action Redressal
                render_actionable_redressal()

            except Exception as e:
                st.error(f"Analysis failed: {e}")

# TAB 2: COMMUNITY SCAM RADAR
with tab_radar:
    st.header("📊 Community Scam Radar (Bharat Telemetry)")
    st.caption("Live, privacy-preserving threat intelligence on emerging financial fraud patterns.")
    
    analytics = get_radar_analytics()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scams Intercepted", analytics["total_scans"])
    col2.metric("High-Risk Schemes Flagged", analytics["high_risk_scans"])
    intercept_rate = int((analytics["high_risk_scans"] / max(1, analytics["total_scans"])) * 100)
    col3.metric("Scam Detection Rate", f"{intercept_rate}%")
    
    st.subheader("⚠️ Top Fraud Vectors Reported This Week")
    for flag, freq in analytics["top_flags"]:
        st.markdown(f"- **{flag}** ({freq} reports)")
        
    st.subheader("🕒 Recent Anonymous Verifications")
    for scan in analytics["recent_scans"]:
        badge = "🔴 HIGH" if scan[3] == "HIGH" else ("🟡 MOD" if scan[3] == "MODERATE" else "🟢 LOW")
        st.write(f"`{scan[0]}` | **{scan[1]}** | Risk: {scan[2]}% ({badge}) | Flag: *{scan[4]}*")

# TAB 3: SEBI PLAYBOOK
with tab_rules:
    st.header("📜 SEBI Investor Resilience Playbook")
    st.markdown("""
    ### Mandatory Regulatory Guardrails:
    1. **No Guaranteed Returns:** Under SEBI (Investment Advisers) Regulations, 2013, no intermediary can assure or guarantee a fixed return.
    2. **Official Registration Nomenclature:**
       - `INA` $\rightarrow$ Investment Advisers
       - `INH` $\rightarrow$ Research Analysts
       - `INZ` $\rightarrow$ Stock Brokers
    3. **Official Redressal Channels:**
       - **SCORES Portal:** `scores.sebi.gov.in` (Toll-Free Helpline: 1800 22 7575 / 1800 266 7575)
       - **National Cyber Crime Reporting:** Call **1930** immediately for banking/UPI frauds.
    """)

# Mandatory Public-Good Guardrail Disclaimer (Page 3 Compliance)
st.markdown("---")
st.caption("⚖️ **Statutory Public-Good Notice:** ScamSatark is a non-commercial investor resilience and fraud-interception tool created for the SANGYAN Hackathon. It does not provide trading signals, buy/sell recommendations, stock tips, or commercial monetization funnels.")
