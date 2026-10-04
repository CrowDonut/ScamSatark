"""
app.py - ScamSatark: National Investor Resilience & Deceptive Vector Interception Shield
Built for SANGYAN Hackathon (SEBI, NSDL & IIT BHU)
"""
import os
import streamlit as st
from PIL import Image, ImageDraw
from dotenv import load_dotenv

# Import modular engines
from ui_components import inject_custom_styles, render_institutional_header, render_risk_verdict, render_statutory_actions
from ai_scanner import analyze_image_for_scams, analyze_voice_query_for_scams
from voice_engine import INDIC_LANGUAGES, generate_regional_audio, get_bhashini_pipeline_metadata
from sebi_rules import audit_sebi_compliance
from database import init_db, log_scan, get_radar_analytics

# System initialization
load_dotenv()
init_db()

st.set_page_config(
    page_title="ScamSatark | SEBI Investor Resilience Shield",
    page_icon="🛡️",
    layout="wide"
)

inject_custom_styles()
render_institutional_header()

# Top Navigation: Language Selection across 12 Indic Languages
lang_col1, lang_col2 = st.columns([1, 3])
with lang_col1:
    selected_lang = st.selectbox(
        "🌐 भाषा चुनें / Select Language:",
        list(INDIC_LANGUAGES.keys()),
        index=0
    )
with lang_col2:
    st.info("💡 **भारत-प्रथम (Bharat-First):** ग्रामीण एवं छोटे शहरों (Tier-2/3) के निवेशकों के लिए 12 भारतीय भाषाओं एवं वॉइस-सपोर्ट युक्त जनहित प्रणाली।")

# Pre-loaded Demo Scenarios for Instant Testing
st.sidebar.header("🧪 निर्णायक मंडल परीक्षण (Judge Demo Simulator)")
st.sidebar.caption("बिना कोई फाइल अपलोड किए तुरंत जांचने के लिए नीचे चुनें:")
sample_choice = st.sidebar.radio(
    "परीक्षण परिदृश्य (Test Scenario):",
    [
        "None (मैन्युअल जांच / Custom Upload)",
        "Scenario 1: Telegram VIP 200% Profit Scam (अवैध गारंटी)",
        "Scenario 2: Fake SEBI Recovery Letter (फर्जी रिकवरी लेटर)",
        "Scenario 3: Legitimate Registered Broker Advisory (वैध सूचना)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**🏛️ नियामक संस्थाएं (Collaborators):**
- भारतीय प्रतिभूति और विनिमय बोर्ड (SEBI)
- नेशनल सिक्योरिटीज डिपॉजिटरी लिमिटेड (NSDL)
- Science & Technology Council, IIT (BHU)
""")

def create_sample_image(scenario_type: str) -> Image.Image:
    """Generates synthetic scam evidence images with high-contrast text."""
    img = Image.new("RGB", (700, 340), color="#0F172A")
    draw = ImageDraw.Draw(img)
    
    if "Scenario 1" in scenario_type:
        text = "⚡ VIP INTRADAY OPTION SIGNALS ⚡\nJoin Premium VIP Group! Guaranteed 200% daily profit.\nDeposit Rs. 15,000 to UPI: profit_guru@oksbi\nSEBI Reg No: SEBI/VIP/2026/PRO\nOnly 2 slots left! Send screenshot after payment."
        draw.text((30, 40), text, fill="#F87171")
    elif "Scenario 2" in scenario_type:
        text = "GOVERNMENT OF INDIA - INVESTOR COMPENSATION WING\nDear Investor, your trapped F&O losses of Rs 92,000\nhave been approved for recovery under SEBI Guaranteed Relief Scheme.\nPay release documentation fee of Rs 4,999 to Admin UPI.\nSEBI Clearance Reg: INA999999999-VIP"
        draw.text((30, 40), text, fill="#FBBF24")
    else:
        text = "ABC CAPITAL SERVICES (SEBI Reg: INZ000123456)\nStatutory Investor Cautionary Advisory:\nSecurities investments are subject to market risks.\nRead all scheme documents carefully before committing funds.\nSEBI registered intermediaries never promise guaranteed returns."
        draw.text((30, 40), text, fill="#34D399")
        
    return img

# Primary Application Tabs
tab_inspect, tab_voice, tab_radar, tab_bhashini, tab_guardrails = st.tabs([
    "📸 फोटो / स्क्रीनशॉट जांच (Image Scan)",
    "🎙️ बोल कर पूछें (Voice Query / Audio)",
    "📊 राष्ट्रीय थ्रेट रडार (Scam Radar)",
    "🇮🇳 भाषिणी DPI आर्किटेक्चर (Bhashini DPI)",
    "📜 SEBI वैधानिक नियम (Statutory Rules)"
])

# -------------------------------------------------------------
# TAB 1: SCREENSHOT FORENSIC INSPECTOR
# -------------------------------------------------------------
with tab_inspect:
    st.subheader("1. स्क्रीनशॉट या विज्ञापन की सत्यता जांचें (Inspect Screenshot / Chat)")
    st.caption("टेलीग्राम, व्हाट्सएप, यूट्यूब या इंस्टाग्राम पर मिले किसी भी मैसेज या विज्ञापन का स्क्रीनशॉट अपलोड करें:")
    
    active_image = None
    if sample_choice != "None (मैन्युअल जांच / Custom Upload)":
        active_image = create_sample_image(sample_choice)
        st.warning(f"परीक्षण मोड सक्रिय: **{sample_choice}** लोड किया गया है।")
        st.image(active_image, caption="Simulated Scam Evidence", use_container_width=True)
    else:
        uploaded_file = st.file_uploader("स्क्रीनशॉट चुनें (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            active_image = Image.open(uploaded_file)
            st.image(active_image, caption="Uploaded Evidence", use_container_width=True)
            
    if active_image and st.button("🔍 जोखिम एवं वैधानिक जांच करें (Verify Scam Risk)", type="primary", use_container_width=True):
        with st.spinner("AI विज़न एवं SEBI वैधानिक नियमों के आधार पर जांच की जा रही है..."):
            try:
                # 1. Multimodal AI Scan
                ai_data = analyze_image_for_scams(active_image, selected_lang)
                
                # 2. Statutory SEBI Regulatory Check
                sebi_data = audit_sebi_compliance(ai_data.get("raw_text", ""))
                
                # 3. Composite Risk Calculation
                final_score = min(100, max(ai_data.get("ai_risk_score", 0), sebi_data.get("regulatory_penalty", 0)))
                final_level = "HIGH" if final_score >= 70 else ("MODERATE" if final_score >= 40 else "LOW")
                
                # 4. Anonymous Logging to Telemetry Database
                primary_flag = (ai_data.get("red_flags") or sebi_data.get("violations") or ["Unverified advisory"])[0]
                log_scan("Telegram/WhatsApp", final_score, final_level, primary_flag, selected_lang)
                
                # 5. Visual Verdict Card
                render_risk_verdict(
                    final_score,
                    final_level,
                    ai_data.get("confidence_score", 88),
                    ai_data.get("uncertainty_rationale", "Visual inspection of text and payment handles")
                )
                
                # Regional Audio Player (Bharat-First Voice Explanation)
                st.markdown("---")
                st.subheader(f"🔊 आपकी भाषा में वॉइस स्पष्टीकरण ({selected_lang}):")
                explanation_text = ai_data.get("plain_explanation_regional") or ai_data.get("plain_explanation_english", "")
                st.info(f"🗣️ *\"{explanation_text}\"*")
                
                audio_path = generate_regional_audio(explanation_text, selected_lang)
                if audio_path and os.path.exists(audio_path):
                    st.audio(audio_path, format="audio/mp3")
                
                # Breakdown Columns
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### 🚩 पहचाने गए भ्रामक संकेत (Red Flags):")
                    for flag in ai_data.get("red_flags", []):
                        st.markdown(f"- ⚠️ **{flag}**")
                        
                with col_b:
                    st.markdown("#### ⚖️ SEBI विनियामक उल्लंघन (Statutory Breaches):")
                    violations = sebi_data.get("violations", []) + ai_data.get("sebi_violations", [])
                    if violations:
                        for v in list(set(violations)):
                            st.markdown(f"- 🚫 **{v}**")
                    else:
                        st.write("कोई प्रत्यक्ष वैधानिक उल्लंघन नहीं पाया गया।")
                        
                # Registration Format Breakdown
                reg_status = sebi_data.get("registration_status", {})
                if reg_status.get("found"):
                    if reg_status.get("is_valid_format"):
                        st.success(f"वैध SEBI रजिस्ट्रेशन प्रारूप: `{reg_status['raw_string']}` ({reg_status['category']})")
                    else:
                        st.error(f"फर्जी / अमान्य SEBI रजिस्ट्रेशन दावा: `{reg_status['raw_string']}` (SEBI का आधिकारिक नंबर प्रारूप नहीं है)")
                
                # Pre-drafted Complaint Box for SCORES 2.0
                st.markdown("---")
                st.subheader("📝 तैयार शिकायत प्रारूप (Pre-Drafted Complaint for SCORES / 1930):")
                complaint = ai_data.get("pre_drafted_complaint", "No complaint draft needed.")
                st.code(complaint, language="text")
                st.caption("इस प्रारूप को कॉपी करके सीधे SEBI SCORES 2.0 या 1930 पोर्टल पर साक्ष्य के रूप में दर्ज किया जा सकता है।")
                
                render_statutory_actions()

            except Exception as e:
                st.error(f"जांच के दौरान तकनीकी त्रुटि: {e}")

# -------------------------------------------------------------
# TAB 2: VOICE-FIRST BHARAT QUERY (SPEAK OR AUDIO NOTE)
# -------------------------------------------------------------
with tab_voice:
    st.subheader("2. बोल कर या पूछ कर जांचें (Voice-First Regional Query)")
    st.caption("यदि आप टाइप नहीं करना चाहते, तो बोलें या अपनी भाषा में सवाल पूछें:")
    
    voice_query_text = st.text_area(
        "अपना सवाल या ऑडियो ट्रांसक्रिप्शन यहाँ लिखें / बोलें:",
        placeholder="उदाहरण: मुझे एक व्हाट्सएप ग्रुप में बोला गया कि ₹10,000 जमा करने पर 7 दिन में ₹30,000 पक्का मिलेगा। क्या यह सुरक्षित है?",
        height=100
    )
    
    # Preset Audio Queries
    st.markdown("**या आम सवालों में से चुनें:**")
    quick_q = st.radio(
        "त्वरित उदाहरण प्रश्न:",
        [
            "कस्टम सवाल लिखें",
            "व्हाट्सएप पर 200% गारंटीड रिटर्न का वादा किया जा रहा है।",
            "एक व्यक्ति कह रहा है कि वह SEBI अप्रूव्ड है और पर्सनल UPI पर पैसा मांग रहा है।",
            "टेलीग्राम पर F&O की 100% श्योर-शॉट कॉल दी जा रही है ₹2000 फीस लेकर।"
        ]
    )
    
    final_query = voice_query_text if quick_q == "कस्टम सवाल लिखें" else quick_q
    
    if st.button("🎙️ आवाज एवं सलाह की जांच करें (Analyze Voice Query)", type="primary"):
        if not final_query.strip():
            st.error("कृपया कोई प्रश्न लिखें या बोलें!")
        else:
            with st.spinner("आवाज एवं भाषा का विश्लेषण किया जा रहा है..."):
                try:
                    res = analyze_voice_query_for_scams(final_query, selected_lang)
                    
                    render_risk_verdict(
                        res.get("ai_risk_score", 85),
                        res.get("ai_risk_level", "HIGH"),
                        res.get("confidence_score", 90),
                        res.get("uncertainty_rationale", "Verbal inquiry forensic evaluation")
                    )
                    
                    st.subheader(f"🔊 ऑडियो सलाह सुनें ({selected_lang}):")
                    voice_resp = res.get("plain_explanation_regional") or res.get("plain_explanation_english", "")
                    st.info(f"🗣️ *\"{voice_resp}\"*")
                    
                    audio_out = generate_regional_audio(voice_resp, selected_lang)
                    if audio_out and os.path.exists(audio_out):
                        st.audio(audio_out, format="audio/mp3")
                        
                    st.markdown("#### 🚩 मुख्य खतरे (Deceptive Markers):")
                    for flag in res.get("red_flags", []):
                        st.markdown(f"- ⚠️ **{flag}**")
                        
                    render_statutory_actions()
                except Exception as e:
                    st.error(f"विश्लेषण विफल: {e}")

# -------------------------------------------------------------
# TAB 3: NATIONAL COMMUNITY SCAM RADAR
# -------------------------------------------------------------
with tab_radar:
    st.subheader("📊 राष्ट्रीय कम्युनिटी स्कैम रडार (National Threat Radar)")
    st.caption("गोपनीयता-संरक्षित टेलीमेट्री: भारत भर में रोके गए वित्तीय धोखाधड़ी के लाइव आंकड़े।")
    
    analytics = get_radar_analytics()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("कुल जांची गई योजनाएं", analytics["total_scans"])
    col2.metric("अवैध / उच्च जोखिम वाली योजनाएं", analytics["high_risk_scans"])
    intercept_rate = int((analytics["high_risk_scans"] / max(1, analytics["total_scans"])) * 100)
    col3.metric("धोखाधड़ी पहचान दर", f"{intercept_rate}%")
    
    st.markdown("---")
    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown("#### 📱 मुख्य धोखाधड़ी वाले माध्यम (Top Vector Platforms)")
        for plat, cnt in analytics["top_platforms"]:
            st.write(f"- **{plat}**: `{cnt} मामले दर्ज`")
            
    with col_y:
        st.markdown("#### ⚠️ सबसे आम फर्जी दावे (Top Fraud Patterns)")
        for flag, cnt in analytics["top_flags"]:
            st.write(f"- **{flag}**: `{cnt} बार पहचाना गया`")
            
    st.markdown("---")
    st.markdown("#### 🕒 हाल की गुमनाम जांचें (Recent Anonymous Verifications)")
    for s in analytics["recent_scans"]:
        tag = "🔴 HIGH" if s[3] == "HIGH" else ("🟡 MOD" if s[3] == "MODERATE" else "🟢 LOW")
        st.write(f"`{s[0]}` | **{s[1]}** | जोखिम: {s[2]}% ({tag}) | कारण: *{s[4]}*")

# -------------------------------------------------------------
# TAB 4: BHASHINI & DIGITAL PUBLIC INFRASTRUCTURE (DPI)
# -------------------------------------------------------------
with tab_bhashini:
    st.subheader("🇮🇳 भाषिणी एवं डिजिटल पब्लिक इन्फ्रास्ट्रक्चर (DPI) एकीकरण")
    st.caption("इलेक्ट्रॉनिक्स और सूचना प्रौद्योगिकी मंत्रालय (MeitY) के राष्ट्रीय भाषा मिशन के अनुरूप आर्किटेक्चर।")
    
    meta = get_bhashini_pipeline_metadata()
    
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:18px;">
        <h4 style="color:#0B2545; margin-top:0;">DPI Integration Specifications:</h4>
        <ul>
            <li><b>DPI Provider:</b> {meta['dpi_provider']}</li>
            <li><b>Supported Indic Languages:</b> 12 भारतीय भाषाएं (Hindi, Marathi, Bengali, Telugu, Tamil, Gujarati, Kannada, Malayalam, Punjabi, Odia, Urdu, English)</li>
            <li><b>Speech Recognition (ASR):</b> Bhashini Indic-Conformer Speech-to-Text Pipeline</li>
            <li><b>Speech Synthesis (TTS):</b> Bhashini Indic-VITS Regional Neural Audio</li>
            <li><b>Translation Layer (NMT):</b> Bhashini Indic-Trans2 Direct Translation</li>
            <li><b>Regulatory Verification:</b> SEBI SCORES 2.0 Intermediary Registry API Hooks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    #### 💡 छोटे शहरों (Tier-2/3) के लिए कम-बैंडविड्थ एवं सुलभता लाभ:
    1. **शून्य तकनीकी जटिलता:** बिना किसी टाइपिंग के सिर्फ आवाज रिकॉर्ड करके पूरी जांच संभव।
    2. **स्थानीय उपमाएं (Analogies):** जटिल अंग्रेजी वित्तीय शब्दों (NAV, Derivates, P/E) के बदले रोजमर्रा की सरल उपमाओं में सीख।
    3. **गोपनीयता आधारित डिजाइन:** किसी भी यूजर का फोन नंबर, बैंक खाता या OTP कभी स्टोर नहीं होता।
    """)

# -------------------------------------------------------------
# TAB 5: SEBI STATUTORY GUARDRAILS
# -------------------------------------------------------------
with tab_guardrails:
    st.subheader("📜 SEBI एवं NSDL वैधानिक सुरक्षा प्लेबुक")
    st.markdown("""
    ### महत्वपूर्ण विनियामक नियम (Mandatory Investor Protections):
    1. **मुनाफे की कोई गारंटी नहीं (No Guaranteed Returns):** SEBI (Investment Advisers) Regulations, 2013 के अनुसार कोई भी रजिस्टर्ड मध्यस्थ मुनाफे की गारंटी नहीं दे सकता।
    2. **वैध रजिस्ट्रेशन संख्या की पहचान:**
       - `INA` + 9 अंक = इन्वेस्टमेंट एडवाइजर (IA)
       - `INH` + 9 अंक = रिसर्च एनालिस्ट (RA)
       - `INZ` + 9 अंक = स्टॉक ब्रोकर
    3. **व्यक्तिगत खातों में भुगतान निषेध:** ब्रोकरेज या एडवाइजरी शुल्क कभी भी किसी व्यक्ति के व्यक्तिगत बचत खाते या निजी UPI आईडी पर नहीं भेजा जाता।
    """)

# Mandatory Non-Commercial Public Good Notice (Charter Page 3 Compliance)
st.markdown("---")
st.caption("⚖️ **वैधानिक सार्वजनिक-हित सूचना (Statutory Public-Good Notice):** ScamSatark एक गैर-व्यावसायिक जनहित सुरक्षा प्लेटफ़ॉर्म है जिसे SANGYAN हैकथॉन के तहत विकसित किया गया है। यह प्लेटफ़ॉर्म किसी भी प्रकार की स्टॉक टिप्स, ट्रेडिंग सिग्नल, शेयर खरीदने-बेचने की सलाह या व्यावसायिक वित्तीय उत्पाद प्रदान नहीं करता है।")
