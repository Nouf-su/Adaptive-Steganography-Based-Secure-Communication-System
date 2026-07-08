""" 
User Interface (Streamlit) - Adaptive Steganography System. 
Full system visible: Text Analysis → Classification → Encryption → Steganography. 
 
Run from terminal:  streamlit run app.py 
Do not run with:    python app.py  (causes "missing ScriptRunContext" warnings) 
""" 
import io 
import sys
import hashlib
from datetime import datetime
 
import streamlit as st

from classification import classify_message
from encryption import encrypt, decrypt
from steganography import embed_message, extract_message


# Must run with "streamlit run app.py" — not "python app.py" 
try: 
    from streamlit.runtime.scriptrunner_utils import get_script_run_ctx 
    if get_script_run_ctx() is None: 
        print("\n  Run the app with:  streamlit run app.py") 
        print("  (Do not use: python app.py)\n") 
        sys.exit(1) 
except Exception:
    pass

st.set_page_config(
    page_title="SecureStego - Adaptive Steganography",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---- Modern Tech Blue Theme with Glassmorphism ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 25%, #F8FAFC 50%, #E0F2FE 75%, #F0F9FF 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.08), 0 2px 8px rgba(30, 58, 138, 0.04) !important;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1E3A8A 0%, #312E81 50%, #1E40AF 100%);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(30, 58, 138, 0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 3rem;
    }
    
    .hero-text h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;
        margin: 0 0 0.75rem 0;
        letter-spacing: -0.02em;
    }
    
    .hero-text p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        margin: 0;
        font-weight: 400;
    }
    
    .hero-badges {
        display: flex;
        gap: 12px;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .hero-badge {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 50px;
        padding: 6px 16px;
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.8rem;
        font-weight: 500;
        backdrop-filter: blur(4px);
    }
    
    .hero-graphics {
        flex-shrink: 0;
    }

    /* Process Flow */
    .process-flow {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .process-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    
    .process-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.35);
        transition: transform 0.3s ease;
    }
    
    .process-icon:hover {
        transform: translateY(-4px);
    }
    
    .process-icon.step-2 { background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%); }
    .process-icon.step-3 { background: linear-gradient(135deg, #059669 0%, #10B981 100%); box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35); }
    .process-icon.step-4 { background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%); box-shadow: 0 8px 24px rgba(139, 92, 246, 0.35); }
    
    .process-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #374151;
    }
    
    .process-arrow {
        color: #9CA3AF;
        font-size: 1.25rem;
    }

    /* Action Cards */
    .action-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 24px;
        padding: 2rem;
        height: 100%;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.08);
        transition: all 0.3s ease;
    }
    
    .action-card:hover {
        box-shadow: 0 12px 48px rgba(30, 58, 138, 0.12);
        transform: translateY(-2px);
    }
    
    .action-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    
    .action-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .action-icon.hide { background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%); }
    .action-icon.extract { background: linear-gradient(135deg, #059669 0%, #10B981 100%); }
    
    .action-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 0;
    }
    
    .action-subtitle {
        font-size: 0.85rem;
        color: #6B7280;
        margin: 4px 0 0 0;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-secondary"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #312E81 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(30, 58, 138, 0.25) !important;
    }
    
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #312E81 0%, #1E3A8A 100%) !important;
        box-shadow: 0 6px 24px rgba(30, 58, 138, 0.35) !important;
        transform: translateY(-2px);
    }
    
    .btn-success {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%) !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
    }
    
    .btn-success:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.4) !important;
    }

    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
        background: #fff !important;
    }
    
    .stTextArea > div > div > textarea { min-height: 120px !important; }

    /* File Upload Zone */
    [data-testid="stFileUploader"] {
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stFileUploader"] > section {
        background: rgba(255, 255, 255, 0.7) !important;
        border: 2px dashed #CBD5E1 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"] > section:hover {
        border-color: #3B82F6 !important;
        background: rgba(59, 130, 246, 0.05) !important;
    }
    
    [data-testid="stFileUploader"] > section > div > div > span {
        color: #6B7280 !important;
        font-size: 0.9rem !important;
    }

    /* Info Cards */
    .info-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 0.75rem 0;
    }
    
    .info-card .label {
        font-size: 0.75rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .info-card .value {
        font-size: 1rem;
        font-weight: 600;
        color: #1E3A8A;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.4rem 0.9rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-public {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46;
        border: 1px solid #6EE7B7;
    }
    
    .badge-restricted {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        color: #92400E;
        border: 1px solid #FCD34D;
    }
    
    .badge-confidential {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A8A 0%, #312E81 100%) !important;
    }
    
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 10px !important;
    }

    /* Section Titles */
    .section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #374151;
        margin: 1rem 0 0.75rem;
    }

    /* Detectors */
    .detectors {
        font-size: 0.8rem;
        color: #6B7280;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #E5E7EB;
    }

    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1E3A8A 0%, #312E81 100%);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-top: 2rem;
    }

    /* Hide default elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Auth Card */
    .auth-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 24px;
        padding: 2.5rem;
        max-width: 500px;
        margin: 2rem auto;
        box-shadow: 0 16px 48px rgba(30, 58, 138, 0.15);
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-header h2 {
        color: #1E3A8A;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .auth-header p {
        color: #6B7280;
        margin: 0;
    }

    /* Radio buttons */
    [data-testid="stRadio"] label {
        color: #374151 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stRadio"] [aria-checked="true"] div:first-child {
        background-color: #3B82F6 !important;
        border-color: #3B82F6 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# AUTH SYSTEM
# ==============================

import json
import os

USERS_FILE = "users.json"

SECURITY_QUESTIONS = [
    "What was the name of your first pet?",
    "What is your mother's maiden name?",
    "What was the name of your primary school?",
    "What is your favorite childhood movie?",
    "What city were you born in?",
]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    # Default built-in accounts
    default = {
        "admin": {
            "password": hash_password("1234"),
            "security_question": "What was the name of your first pet?",
            "security_answer": hash_password("fluffy"),
        },
        "user": {
            "password": hash_password("abcd"),
            "security_question": "What city were you born in?",
            "security_answer": hash_password("riyadh"),
        },
    }
    save_users(default)
    return default

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def show_auth():
    # Hero Section with 3D Graphics
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-text">
                <h1>🔐 SecureStego</h1>
                <p>Adaptive Steganography System with AI-Powered Security</p>
                <div class="hero-badges">
                    <span class="hero-badge">🔒 End-to-End Encrypted</span>
                    <span class="hero-badge">🛡️ NCA Compliant</span>
                    <span class="hero-badge">🤖 AI-Powered</span>
                </div>
            </div>
            <div class="hero-graphics">
                <svg width="180" height="180" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#60A5FA;stop-opacity:0.9" />
                            <stop offset="50%" style="stop-color:#3B82F6;stop-opacity:0.8" />
                            <stop offset="100%" style="stop-color:#1D4ED8;stop-opacity:0.9" />
                        </linearGradient>
                        <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#34D399;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#10B981;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <path d="M90 20L160 55V115L90 150L20 115V55L90 20Z" fill="url(#shieldGrad)" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
                    <path d="M90 20L160 55L90 90L20 55L90 20Z" fill="rgba(255,255,255,0.2)"/>
                    <path d="M90 90L160 55V115L90 150V90Z" fill="rgba(30,58,138,0.3)"/>
                    <path d="M90 90L20 55V115L90 150V90Z" fill="rgba(59,130,246,0.3)"/>
                    <rect x="70" y="75" width="40" height="35" rx="5" fill="url(#accentGrad)"/>
                    <path d="M78 75V65C78 58 83 52 90 52C97 52 102 58 102 65V75" stroke="#059669" stroke-width="4" fill="none"/>
                    <circle cx="90" cy="92" r="4" fill="white"/>
                    <text x="35" y="100" fill="rgba(255,255,255,0.4)" font-family="monospace" font-size="8">1010</text>
                    <text x="125" y="100" fill="rgba(255,255,255,0.4)" font-family="monospace" font-size="8">0101</text>
                    <text x="45" y="125" fill="rgba(255,255,255,0.3)" font-family="monospace" font-size="6">110011</text>
                    <text x="115" y="125" fill="rgba(255,255,255,0.3)" font-family="monospace" font-size="6">001100</text>
                </svg>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Process Flow
    st.markdown("""
    <div class="glass-card" style="padding: 1.5rem; margin-bottom: 2rem;">
        <div class="process-flow" style="margin: 0;">
            <div class="process-step">
                <div class="process-icon">📝</div>
                <div class="process-label">Text Analysis</div>
            </div>
            <div class="process-arrow">→</div>
            <div class="process-step">
                <div class="process-icon step-2">🎯</div>
                <div class="process-label">Classification</div>
            </div>
            <div class="process-arrow">→</div>
            <div class="process-step">
                <div class="process-icon step-3">🔐</div>
                <div class="process-label">Encryption</div>
            </div>
            <div class="process-arrow">→</div>
            <div class="process-step">
                <div class="process-icon step-4">🖼️</div>
                <div class="process-label">Steganography</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auth Card
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="auth-header">
        <h2>Welcome Back</h2>
        <p>Sign in to access the secure steganography system</p>
    </div>
    """, unsafe_allow_html=True)

    users = load_users()

    auth_tab = st.radio(
        "Choose an option",
        ["Login", "Create Account", "Forgot Password"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- LOGIN ----
    if auth_tab == "Login":
        username = st.text_input("👤 Username", key="login_user", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", key="login_pass", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In", type="primary", use_container_width=True):
            if username in users and users[username]["password"] == hash_password(password):
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    # ---- SIGN UP ----
    elif auth_tab == "Create Account":
        new_user = st.text_input("👤 Choose a username", key="reg_user", placeholder="Create a username")
        new_pass = st.text_input("🔑 Choose a password", type="password", key="reg_pass", placeholder="Create a password")
        confirm_pass = st.text_input("🔑 Confirm password", type="password", key="reg_confirm", placeholder="Confirm your password")
        sec_q = st.selectbox("❓ Security question", SECURITY_QUESTIONS, key="reg_sec_q")
        sec_a = st.text_input("💡 Your answer", key="reg_sec_a", placeholder="Answer for account recovery")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create Account", type="primary", use_container_width=True):
            if not new_user or not new_pass or not sec_a:
                st.warning("⚠️ Please fill in all fields.")
            elif new_user in users:
                st.error("❌ Username already exists. Please choose another.")
            elif new_pass != confirm_pass:
                st.error("❌ Passwords do not match.")
            elif len(new_pass) < 4:
                st.warning("⚠️ Password must be at least 4 characters.")
            else:
                users[new_user] = {
                    "password": hash_password(new_pass),
                    "security_question": sec_q,
                    "security_answer": hash_password(sec_a.strip().lower()),
                }
                save_users(users)
                st.success(f"✅ Account created successfully! You can now login as **{new_user}**.")

    # ---- FORGOT PASSWORD ----
    elif auth_tab == "Forgot Password":
        username = st.text_input("👤 Enter your username", key="fp_user", placeholder="Your username")

        if username:
            users = load_users()
            if username not in users:
                st.error("❌ No account found with that username.")
            else:
                sec_q = users[username]["security_question"]
                st.info(f"**❓ Security Question:** {sec_q}")
                sec_a = st.text_input("💡 Your answer", key="fp_answer", placeholder="Your security answer")
                new_pass = st.text_input("🔑 New password", type="password", key="fp_new", placeholder="Enter new password")
                confirm_pass = st.text_input("🔑 Confirm new password", type="password", key="fp_confirm", placeholder="Confirm new password")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset Password", type="primary", use_container_width=True):
                    if not sec_a or not new_pass:
                        st.warning("⚠️ Please fill in all fields.")
                    elif users[username]["security_answer"] != hash_password(sec_a.strip().lower()):
                        st.error("❌ Incorrect answer. Please try again.")
                    elif new_pass != confirm_pass:
                        st.error("❌ Passwords do not match.")
                    elif len(new_pass) < 4:
                        st.warning("⚠️ Password must be at least 4 characters.")
                    else:
                        users[username]["password"] = hash_password(new_pass)
                        save_users(users)
                        st.success("✅ Password reset successfully! You can now login with your new password.")

    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.rerun()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    show_auth()
    st.stop()


# ==============================
# 🧾 LOGGING SYSTEM
# ==============================

LOG_FILE = "logs.txt"

def log_event(action):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = st.session_state.get("user", "unknown")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] ({user}) {action}\n")

def show_logs():
    st.markdown("""
    <div class="main-header">
        <span class="icon-main">📜</span>
        <h1>Security Logs</h1>
        <p>Latest recorded events</p>
    </div>
    """, unsafe_allow_html=True)
    try:
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
        for log in reversed(logs[-20:]):
            st.text(log.strip())
    except:
        st.info("No logs available")


# ==============================
# 📌 SIDEBAR (Minimal)
# ==============================

st.sidebar.markdown(f"""
<div style="padding: 1rem 0;">
    <div style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 0.5rem;">Logged in as</div>
    <div style="font-size: 1.1rem; font-weight: 600; color: white;">👤 {st.session_state['user']}</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout()

st.sidebar.markdown("<br>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigation",
    ["📝 Hide Message", "📤 Extract Message", "📜 View Logs"],
    label_visibility="collapsed"
)


# ==============================
# 📜 LOGS PAGE
# ==============================

if page == "📜 View Logs":
    show_logs()
    st.stop()


# ==============================
# MAIN APP (Hide / Extract)
# ==============================

# ---- Modern Header ----
st.markdown("""
<div class="hero-section" style="padding: 2rem 2.5rem;">
    <div class="hero-content">
        <div class="hero-text">
            <h1 style="font-size: 2rem;">🔐 SecureStego Dashboard</h1>
            <p>Secure Message Hiding & Extraction System</p>
            <div class="hero-badges">
                <span class="hero-badge">🛡️ NCA Compliant</span>
                <span class="hero-badge">🔒 End-to-End Encrypted</span>
                <span class="hero-badge">🤖 AI-Powered Classification</span>
            </div>
        </div>
        <div class="hero-graphics">
            <svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="dashGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#60A5FA;stop-opacity:0.9" />
                        <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:0.8" />
                    </linearGradient>
                </defs>
                <circle cx="60" cy="60" r="50" stroke="rgba(255,255,255,0.2)" stroke-width="2" fill="none"/>
                <circle cx="60" cy="60" r="35" stroke="url(#dashGrad)" stroke-width="3" fill="none" stroke-dasharray="8 4"/>
                <rect x="45" y="45" width="30" height="30" rx="6" fill="rgba(255,255,255,0.9)"/>
                <path d="M52 58L57 63L68 52" stroke="#1E40AF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Process Flow ----
st.markdown("""
<div class="glass-card" style="padding: 1.5rem; margin-bottom: 2rem;">
    <div class="process-flow" style="margin: 0;">
        <div class="process-step">
            <div class="process-icon">📝</div>
            <div class="process-label">Text Analysis</div>
        </div>
        <div class="process-arrow">→</div>
        <div class="process-step">
            <div class="process-icon step-2">🎯</div>
            <div class="process-label">Classification</div>
        </div>
        <div class="process-arrow">→</div>
        <div class="process-step">
            <div class="process-icon step-3">🔐</div>
            <div class="process-label">Encryption</div>
        </div>
        <div class="process-arrow">→</div>
        <div class="process-step">
            <div class="process-icon step-4">🖼️</div>
            <div class="process-label">Steganography</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Mode selection ----
if page == "📝 Hide Message":
    mode = "📤 Hide message in image"
else:
    mode = "📥 Extract message from image"

# Reset extract display when switching mode or uploading new file
if "display_message" not in st.session_state:
    st.session_state["display_message"] = None
if "extract_level" not in st.session_state:
    st.session_state["extract_level"] = None

# ---- HIDE MESSAGE ----
if mode == "📤 Hide message in image":
    st.session_state["display_message"] = None
    st.session_state["extract_level"] = None

    st.markdown('''
    <div class="action-card">
        <div class="action-header">
            <div class="action-icon hide">📤</div>
            <div>
                <div class="action-title">Hide Message</div>
                <div class="action-subtitle">Embed a secret message into an image</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<p class="section-title">📝 Message Content</p>', unsafe_allow_html=True)
    message = st.text_area(
        "Type your secret message below",
        height=120,
        placeholder="Enter the message you want to hide inside the image...",
        label_visibility="collapsed",
        key="hide_message",
    )

    st.markdown('<p class="section-title">🖼️ Cover Image</p>', unsafe_allow_html=True)
    cover_file = st.file_uploader(
        "Drag and drop or click to upload image (PNG, JPG)",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
        key="cover_upload",
    )

    if message and cover_file:
        classification = classify_message(message)
        level = classification["level"]
        score = classification["score"]
        actions = classification.get("actions", {})
        triggered = classification.get("triggered_detectors", [])

        st.markdown('<p class="section-title"><span class="sec-icon">🛡️</span> Sensitivity analysis</p>', unsafe_allow_html=True)
        level_class = f"badge-{level.lower()}"
        det_html = f'<div class="detectors">Detected: {", ".join(triggered)}</div>' if triggered else ""
        st.markdown(f""" 
        <div class="info-card"> 
            <div class="label">Classification level</div><div class="value"><span class="badge {level_class}">{level}</span></div> 
            <div class="label" style="margin-top:0.5rem">Risk score</div> 
            <div class="value">{score}</div> 
            {det_html} 
        </div> 
        """, unsafe_allow_html=True)

        log_event(f"Message classified as {level} (Score: {score})")

        password = None
        if actions.get("password"):
            st.markdown(f"**🔑 Password required ({level})**")
            password = st.text_input("Enter password", type="password", label_visibility="visible", key="hide_pwd")

        if st.button("🚀 Hide message in image", type="primary", use_container_width=True):
            try:
                if actions.get("encrypt"):
                    enc_result = encrypt(message, level, password=password)
                    payload = enc_result["data"]
                    if isinstance(payload, str):
                        payload = payload.encode("utf-8")
                    log_event("Encryption applied")
                else:
                    payload = message.encode("utf-8")

                img_bytes = io.BytesIO(cover_file.read())
                out_img = embed_message(img_bytes, payload, output_path=None, level=level)
                if out_img is None:
                    st.error("An error occurred while hiding the message.")
                else:
                    buf = io.BytesIO()
                    out_img.save(buf, format="PNG")
                    buf.seek(0)
                    st.success("Message hidden successfully. Download the stego image below.")
                    log_event("Message embedded into image")
                    st.download_button(
                        label="⬇️ Download stego image",
                        data=buf,
                        file_name="stego_image.png",
                        mime="image/png",
                        type="primary",
                        use_container_width=True,
                        key="dl_stego",
                    )
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error: {e}")

# ---- EXTRACT MESSAGE ----
elif mode == "📥 Extract message from image":
    st.markdown('''
    <div class="action-card">
        <div class="action-header">
            <div class="action-icon extract">📥</div>
            <div>
                <div class="action-title">Extract Message</div>
                <div class="action-subtitle">Retrieve hidden messages from stego images</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<p class="section-title">🖼️ Stego Image</p>', unsafe_allow_html=True)
    stego_file = st.file_uploader(
        "Upload image with hidden message (PNG, JPG)",
        type=["png", "jpg", "jpeg"],
        key="stego_upload",
        label_visibility="collapsed",
    )

    if stego_file:
        if st.session_state.get("last_stego_name") != stego_file.name:
            for key in ("extracted_level", "extracted_data", "extraction_done", "last_stego_name", "display_message", "extract_level"):
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state["last_stego_name"] = stego_file.name

        if st.button("🔍 Extract message", type="primary", use_container_width=True):
            try:
                img_bytes = io.BytesIO(stego_file.read())
                level, data = extract_message(img_bytes)
                st.session_state["extracted_level"] = level
                st.session_state["extracted_data"] = data
                st.session_state["extraction_done"] = True
                st.session_state["display_message"] = None
                st.session_state["extract_level"] = level
                log_event("Message extracted successfully")
            except Exception as e:
                st.error(f"Extraction error: {e}")
                log_event("Extraction failed (wrong password or corrupted data)")

        if st.session_state.get("extraction_done") and "extracted_level" in st.session_state:
            level = st.session_state["extracted_level"]
            data = st.session_state["extracted_data"]
            st.session_state["extract_level"] = level

            st.markdown('<p class="section-title">📋 Extracted Content</p>', unsafe_allow_html=True)
            level_class = f"badge-{level.lower()}"
            st.markdown(f"""
            <div class="info-card">
                <div class="label">Classification Level</div><div class="value"><span class="badge {level_class}">{level}</span></div>
            </div>
            """, unsafe_allow_html=True)
            # ENC_ACTIONS defines encryption requirements per classification level
            ENC_ACTIONS = {
                "Public": {"encrypt": False, "password": False},
                "Restricted": {"encrypt": True, "password": True},
                "Confidential": {"encrypt": True, "password": True},
            }

            actions = ENC_ACTIONS.get(level, ENC_ACTIONS["Public"])

            if not actions["encrypt"]:
                try:
                    text = data.decode("utf-8")
                    st.session_state["display_message"] = text
                except Exception:
                    st.session_state["display_message"] = data.hex() if len(data) < 200 else data[:200].hex() + "..."
            else:
                # Encrypted messages require password for both Restricted and Confidential
                st.markdown("**🔑 Enter password to decrypt**")
                pwd = st.text_input("Password", type="password", key="extract_pwd", label_visibility="visible")
                if st.button("🔓 Decrypt and show message", type="primary", use_container_width=True, key="btn_decrypt"):
                    if pwd:
                        try:
                            decrypted = decrypt({"data": data, "level": level}, password=pwd)
                            st.session_state["display_message"] = decrypted
                            st.rerun()
                        except Exception as e:
                            st.error(f"Decryption failed. Check the password: {e}")
                    else:
                        st.warning("Enter the password first.")

            # ---- Always show message box when we have something to show ----
            if st.session_state.get("display_message") is not None:
                msg = st.session_state["display_message"]
                st.markdown('<p class="section-title">📩 Extracted Message</p>', unsafe_allow_html=True)
                st.text_area(
                    "Message content",
                    value=msg,
                    height=160,
                    disabled=True,
                    label_visibility="collapsed",
                    key="extracted_msg_display",
                )

# ---- Modern Footer ----
st.markdown("""
<div class="footer">
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:20px;">
        <div style="display:flex; align-items:center; gap:24px; flex-wrap:wrap;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:32px;height:32px;background:rgba(255,255,255,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center; backdrop-filter:blur(4px);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                </div>
                <div>
                    <div style="color:rgba(255,255,255,0.9);font-size:12px;font-weight:600;">SecureStego</div>
                    <div style="color:rgba(255,255,255,0.5);font-size:10px;">Enterprise Security Solution</div>
                </div>
            </div>
            <div style="width:1px;height:32px;background:rgba(255,255,255,0.2);"></div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:32px;height:32px;background:rgba(255,255,255,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center; backdrop-filter:blur(4px);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="2">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                        <circle cx="12" cy="5" r="2"/>
                        <path d="M12 7v4"/>
                        <line x1="8" y1="16" x2="8" y2="16"/>
                        <line x1="16" y1="16" x2="16" y2="16"/>
                    </svg>
                </div>
                <div>
                    <div style="color:rgba(255,255,255,0.9);font-size:12px;font-weight:600;">NCA Certified</div>
                    <div style="color:rgba(255,255,255,0.5);font-size:10px;">National Cybersecurity Authority</div>
                </div>
            </div>
            <div style="width:1px;height:32px;background:rgba(255,255,255,0.2);"></div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:32px;height:32px;background:rgba(255,255,255,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center; backdrop-filter:blur(4px);">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                        <path d="M2 17l10 5 10-5"/>
                        <path d="M2 12l10 5 10-5"/>
                    </svg>
                </div>
                <div>
                    <div style="color:rgba(255,255,255,0.9);font-size:12px;font-weight:600;">University Partner</div>
                    <div style="color:rgba(255,255,255,0.5);font-size:10px;">Hafr Al-Batin</div>
                </div>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="color:rgba(255,255,255,0.8);font-size:13px;font-weight:600;">🔐 SecureStego System</div>
            <div style="color:rgba(255,255,255,0.4);font-size:11px;margin-top:4px;">v2.0 • Built with ❤️ for secure communication</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)