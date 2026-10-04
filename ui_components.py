"""
ui_components.py - Institutional Light-Theme & Bharat-First Design System
Clean, authoritative public-good interface inspired by SEBI, NSDL & Bhashini standards.
"""
import streamlit as st

def inject_custom_styles():
    """Injects high-contrast, clean, institutional light-theme CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans Devanagari', -apple-system, sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Institutional Tricolor Header Accent */
    .gov-accent-bar {
        height: 4px;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        border-radius: 2px;
        margin-bottom: 16px;
    }
    
    .inst-header {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 24px;
        text-align: center;
    }
    
    .inst-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0B2545;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .inst-subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-top: 6px;
        font-weight: 500;
    }
    
    .inst-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-top: 12px;
    }
    
    /* Clean Risk Verdict Cards */
    .verdict-high {
        background-color: #FEF2F2;
        border: 2px solid #DC2626;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .verdict-mod {
        background-color: #FFFBEB;
        border: 2px solid #D97706;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .verdict-low {
        background-color: #F0FDF4;
        border: 2px solid #16A34A;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* White Card Wrapper */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    
    /* Clean Pre-drafted Complaint Box */
    .complaint-box {
        background-color: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 14px;
        font-family: monospace;
        font-size: 0.9rem;
        color: #334155;
        white-space: pre-wrap;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 16px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_institutional_header():
    """Renders the official public-good header."""
    st.markdown('<div class="gov-accent-bar"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="inst-header">
        <h1 class="inst-title">🛡️ ScamSatark (स्कैम सतर्क)</h1>
        <p class="inst-subtitle">National Investor Resilience & Deceptive Vector Interception Shield</p>
        <div class="inst-badge">
            🏛️ SEBI & NSDL SANGYAN 2026 • PUBLIC-GOOD INFRASTRUCTURE • BHASHINI DPI POWERED
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_risk_verdict(score: int, level: str, confidence: int, rationale: str):
    """Renders the high-contrast verdict box."""
    if level == "HIGH" or score >= 70:
        st.markdown(f"""
        <div class="verdict-high">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="color:#991B1B; margin:0; font-size:1.6rem;">🚨 उच्च जोखिम (HIGH SCAM RISK): {score}%</h2>
                <span style="background:#DC2626; color:white; padding:4px 12px; border-radius:6px; font-weight:700; font-size:0.85rem;">STATUTORY RED ALERT</span>
            </div>
            <p style="color:#7F1D1D; margin:8px 0 0 0; font-size:1.05rem; font-weight:600;">
                गंभीर धोखाधड़ी और अवैध दावों के स्पष्ट संकेत मिले हैं। किसी भी खाते में पैसा न भेजें।
            </p>
            <div style="margin-top:12px; font-size:0.88rem; color:#991B1B; border-top:1px dashed #FCA5A5; padding-top:8px;">
                🔍 <b>अनिश्चितता और सटीकता (Confidence):</b> AI सटीकता <b>{confidence}%</b> — {rationale}
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif level == "MODERATE" or score >= 40:
        st.markdown(f"""
        <div class="verdict-mod">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="color:#92400E; margin:0; font-size:1.6rem;">⚠️ मध्यम सावधानी (MODERATE CAUTION): {score}%</h2>
                <span style="background:#D97706; color:white; padding:4px 12px; border-radius:6px; font-weight:700; font-size:0.85rem;">VERIFICATION REQUIRED</span>
            </div>
            <p style="color:#78350F; margin:8px 0 0 0; font-size:1.05rem; font-weight:600;">
                यह सामग्री भ्रामक हो सकती है। गैर-प्रमाणित सलाहकारों से सतर्क रहें।
            </p>
            <div style="margin-top:12px; font-size:0.88rem; color:#92400E; border-top:1px dashed #FDE68A; padding-top:8px;">
                🔍 <b>अनिश्चितता और सटीकता (Confidence):</b> AI सटीकता <b>{confidence}%</b> — {rationale}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="verdict-low">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="color:#166534; margin:0; font-size:1.6rem;">✅ सामान्य / कम जोखिम (LOW RISK): {score}%</h2>
                <span style="background:#16A34A; color:white; padding:4px 12px; border-radius:6px; font-weight:700; font-size:0.85rem;">INFORMATIONAL</span>
            </div>
            <p style="color:#14532D; margin:8px 0 0 0; font-size:1.05rem; font-weight:600;">
                कोई स्पष्ट धोखाधड़ी या गैर-कानूनी दावे नहीं पाए गए। आधिकारिक स्रोतों से मिलान करें।
            </p>
            <div style="margin-top:12px; font-size:0.88rem; color:#166534; border-top:1px dashed #BBF7D0; padding-top:8px;">
                🔍 <b>अनिश्चितता और सटीकता (Confidence):</b> AI सटीकता <b>{confidence}%</b> — {rationale}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_statutory_actions():
    """Renders official statutory helpline callouts."""
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:18px; margin-top:20px;">
        <h4 style="margin:0 0 10px 0; color:#0B2545;">🏛️ वैधानिक सुरक्षा एवं शिकायत निवारण (Statutory Redressal):</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px;">
                <strong style="color:#1E3A8A;">1. SEBI SCORES 2.0 पोर्टल</strong><br>
                <span style="font-size:0.88rem; color:#475569;">मध्यस्थों या ब्रोकर्स के खिलाफ आधिकारिक शिकायत दर्ज करें।</span><br>
                <a href="https://scores.sebi.gov.in" target="_blank" style="font-weight:700; color:#2563EB;">scores.sebi.gov.in ↗</a>
            </div>
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px;">
                <strong style="color:#DC2626;">2. राष्ट्रीय साइबर क्राइम हेल्पलाइन (1930)</strong><br>
                <span style="font-size:0.88rem; color:#475569;">यदि बैंक या UPI से राशि कट चुकी है, तुरंत 1930 डायल करें।</span><br>
                <a href="https://cybercrime.gov.in" target="_blank" style="font-weight:700; color:#DC2626;">cybercrime.gov.in ↗</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
