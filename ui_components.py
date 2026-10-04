"""
ui_components.py - Frontend Components and Design System
Provides modern, accessible visual styling tailored for mobile-first Bharat investors.
"""
import streamlit as st

def inject_custom_styles():
    """Injects responsive CSS styles into the Streamlit app."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .hero-title { font-size: 2.2rem; font-weight: 800; margin: 0; color: #FFFFFF; }
    .hero-tagline { font-size: 1rem; color: #93C5FD; margin-top: 6px; }
    .badge-bharat {
        background-color: #F59E0B;
        color: #78350F;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
    }
    .risk-banner-high {
        background: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 18px;
        margin: 20px 0;
    }
    .risk-banner-mod {
        background: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 12px;
        padding: 18px;
        margin: 20px 0;
    }
    .risk-banner-low {
        background: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 12px;
        padding: 18px;
        margin: 20px 0;
    }
    .action-box {
        background: #F8FAFC;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 18px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_hero():
    """Renders the top branding hero banner."""
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🛡️ ScamSatark (स्कैम सतर्क)</h1>
        <p class="hero-tagline">AI-Powered Regional Scam & Misinformation Shield for Bharat</p>
        <span class="badge-bharat">SEBI SANGYAN HACKATHON 2026 • PUBLIC-GOOD INFRASTRUCTURE</span>
    </div>
    """, unsafe_allow_html=True)

def render_risk_gauge(final_score: int, level: str, confidence: int, rationale: str):
    """Renders the visual risk gauge and uncertainty evaluation."""
    if level == "HIGH" or final_score >= 70:
        st.markdown(f"""
        <div class="risk-banner-high">
            <h2 style="color:#B91C1C; margin:0;">🚨 HIGH SCAM RISK: {final_score}%</h2>
            <p style="color:#7F1D1D; margin:6px 0 0 0; font-size:1.05rem;"><b>Status:</b> Severe Deceptive Vectors & Regulatory Violations Detected</p>
            <p style="color:#991B1B; font-size:0.85rem; margin-top:8px;">🔍 <b>Uncertainty Assessment:</b> AI Confidence: <b>{confidence}%</b> ({rationale})</p>
        </div>
        """, unsafe_allow_html=True)
    elif level == "MODERATE" or final_score >= 40:
        st.markdown(f"""
        <div class="risk-banner-mod">
            <h2 style="color:#B45309; margin:0;">⚠️ MODERATE CAUTION: {final_score}%</h2>
            <p style="color:#78350F; margin:6px 0 0 0; font-size:1.05rem;"><b>Status:</b> Unverified Claims or High-Risk Marketing</p>
            <p style="color:#92400E; font-size:0.85rem; margin-top:8px;">🔍 <b>Uncertainty Assessment:</b> AI Confidence: <b>{confidence}%</b> ({rationale})</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="risk-banner-low">
            <h2 style="color:#047857; margin:0;">✅ LOW RISK / INFORMATIONAL: {final_score}%</h2>
            <p style="color:#064E3B; margin:6px 0 0 0; font-size:1.05rem;"><b>Status:</b> No Obvious Fraud Patterns Identified</p>
            <p style="color:#065F46; font-size:0.85rem; margin-top:8px;">🔍 <b>Uncertainty Assessment:</b> AI Confidence: <b>{confidence}%</b> ({rationale})</p>
        </div>
        """, unsafe_allow_html=True)

def render_actionable_redressal():
    """Renders statutory recovery and reporting channels."""
    st.markdown("""
    <div class="action-box">
        <h4 style="margin-top:0; color:#1E293B;">🛡️ Statutory Investor Protection Steps:</h4>
        <ol style="margin-bottom:0; color:#334155; line-height:1.6;">
            <li><b>Do NOT transfer funds:</b> Never send investment deposits to personal UPI IDs or private savings accounts.</li>
            <li><b>Verify on Official SEBI Registry:</b> Check registered intermediaries at <a href="https://www.sebi.gov.in" target="_blank">sebi.gov.in</a>.</li>
            <li><b>Lodge Complaint on SEBI SCORES:</b> Use <a href="https://scores.sebi.gov.in" target="_blank"><b>scores.sebi.gov.in</b></a> for formal complaints against financial market participants.</li>
            <li><b>Report Financial Cyber Crime:</b> If you already sent money, immediately call the National Cyber Crime Helpline at <b>1930</b> or file at <a href="https://cybercrime.gov.in" target="_blank"><b>cybercrime.gov.in</b></a>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
