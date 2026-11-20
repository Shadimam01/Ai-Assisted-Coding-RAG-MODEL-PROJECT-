"""All the styling for the app lives here (CSS + small HTML pieces)."""
import streamlit as st

CSS = """
<style>
:root { color-scheme: dark; }

/* ---------- page background ---------- */
.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(99,102,241,0.28) 0%, transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(236,72,153,0.18) 0%, transparent 35%),
        linear-gradient(180deg, #0b1020 0%, #070a14 100%);
    background-attachment: fixed;
}
.stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #e5e7eb; }
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1100px; }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111634 0%, #0c1024 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] h3 { color: #a5b4fc; font-size: 0.95rem;
    text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.5rem; }
.brand { display:flex; align-items:center; gap:12px; margin: 0.5rem 0 1rem 0; }
.brand .logo { width:44px; height:44px; border-radius:12px; display:flex;
    align-items:center; justify-content:center; font-size:22px;
    background: linear-gradient(135deg,#6366f1,#ec4899);
    box-shadow: 0 6px 20px rgba(99,102,241,0.45); }
.brand .name { font-weight:700; font-size:1.15rem; color:#fff; line-height:1.1; }
.brand .sub { font-size:0.75rem; color:#94a3b8; }

/* ---------- hero ---------- */
.hero { padding: 1.6rem 1.8rem; border-radius: 20px; margin-bottom: 1rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(236,72,153,0.12));
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 10px 40px rgba(0,0,0,0.35); }
.hero h1 { margin:0; font-size: 2rem; font-weight: 800;
    background: linear-gradient(90deg,#c7d2fe,#f9a8d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { margin: 0.4rem 0 0 0; color:#cbd5e1; font-size: 1rem; }

/* ---------- status chips ---------- */
.chips { display:flex; flex-wrap:wrap; gap:8px; margin: 0.2rem 0 1.1rem 0; }
.chip { padding: 5px 12px; border-radius: 999px; font-size: 0.78rem;
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
    color:#e2e8f0; }
.chip.ok   { border-color: rgba(52,211,153,0.5); color:#6ee7b7; background: rgba(16,185,129,0.12); }
.chip.warn { border-color: rgba(251,191,36,0.5); color:#fcd34d; background: rgba(245,158,11,0.12); }

/* ---------- buttons ---------- */
.stButton > button {
    border-radius: 12px; border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.05); color:#e5e7eb; padding: 0.7rem 0.5rem;
    transition: all 0.18s ease; font-weight: 500;
}
.stButton > button:hover {
    border-color: #818cf8; color:#fff; transform: translateY(-2px);
    background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(236,72,153,0.25));
    box-shadow: 0 8px 24px rgba(99,102,241,0.35);
}

/* ---------- welcome card ---------- */
.welcome { padding: 1.2rem 1.5rem; border-radius: 16px; margin: 0.8rem 0;
    background: rgba(255,255,255,0.04); border: 1px dashed rgba(255,255,255,0.18); }
.welcome h4 { margin:0 0 0.5rem 0; color:#fff; }
.welcome ul { margin:0; padding-left: 1.2rem; color:#cbd5e1; }
.welcome li { margin: 0.25rem 0; }

/* ---------- chat ---------- */
div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    backdrop-filter: blur(6px);
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, rgba(99,102,241,0.20), rgba(99,102,241,0.08));
    border-color: rgba(129,140,248,0.35);
}
div[data-testid="stChatInput"] { border-radius: 16px; }
div[data-testid="stChatInput"] textarea { color:#f1f5f9; }
div[data-testid="stBottom"] > div { background: transparent; }

/* ---------- expanders, code, uploader ---------- */
div[data-testid="stExpander"] { border-radius: 12px; border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.03); }
div[data-testid="stFileUploader"] section { border-radius: 14px;
    border: 1.5px dashed rgba(129,140,248,0.5); background: rgba(99,102,241,0.07); }
pre, code { border-radius: 10px !important; }
/* ---------- login / forms / tabs ---------- */
div[data-testid="stForm"] { border-radius: 18px; padding: 1.4rem 1.4rem 1rem 1.4rem;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 40px rgba(0,0,0,0.35); }
div[data-baseweb="input"] { border-radius: 10px; }
button[data-baseweb="tab"] { font-weight: 600; }
.login-hero { text-align:center; margin: 2.5rem 0 1.2rem 0; }
.login-hero .logo { width:70px; height:70px; border-radius:20px; margin: 0 auto 14px auto;
    display:flex; align-items:center; justify-content:center; font-size:34px;
    background: linear-gradient(135deg,#6366f1,#ec4899);
    box-shadow: 0 10px 30px rgba(99,102,241,0.5); }
.login-hero h1 { margin:0; font-size:2rem; font-weight:800;
    background: linear-gradient(90deg,#c7d2fe,#f9a8d4);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.login-hero p { color:#94a3b8; margin:0.4rem 0 0 0; }

/* ---------- user badge, stat cards ---------- */
.user-badge { display:flex; align-items:center; gap:10px; padding:10px 12px; margin-bottom:10px;
    border-radius:12px; background: rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.10); }
.user-badge .avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center;
    justify-content:center; font-weight:700; color:#fff; background: linear-gradient(135deg,#6366f1,#ec4899); }
.user-badge .uname { font-weight:600; color:#fff; line-height:1.1; }
.user-badge .role { font-size:0.72rem; color:#a5b4fc; text-transform:uppercase; letter-spacing:0.08em; }
.stats { display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin: 0.4rem 0 1rem 0; }
.stat { padding: 14px 16px; border-radius:14px; background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.10); }
.stat .num { font-size:1.7rem; font-weight:800; color:#fff; }
.stat .lbl { font-size:0.78rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.06em; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_brand():
    st.markdown(
        '<div class="brand"><div class="logo">📘</div>'
        '<div><div class="name">Tech Doc Assistant</div>'
        '<div class="sub">RAG chatbot for engineers</div></div></div>',
        unsafe_allow_html=True,
    )


def hero():
    st.markdown(
        '<div class="hero"><h1>Technical Documentation Assistant</h1>'
        '<p>Ask about your company docs, or upload an error log or spec and get a fix.</p></div>',
        unsafe_allow_html=True,
    )


def chips(provider, mode, files_count, kb_ready):
    kb = '<span class="chip ok">Knowledge base ready</span>' if kb_ready \
        else '<span class="chip warn">Knowledge base empty</span>'
    files = f'<span class="chip ok">{files_count} file(s) uploaded</span>' if files_count \
        else '<span class="chip">No file uploaded</span>'
    st.markdown(
        f'<div class="chips"><span class="chip">🤖 {provider}</span>'
        f'<span class="chip">📂 Source: {mode}</span>{files}{kb}</div>',
        unsafe_allow_html=True,
    )


def welcome():
    st.markdown(
        '<div class="welcome"><h4>How to get started</h4><ul>'
        '<li>Ask: <i>"What is our naming convention for REST endpoints?"</i></li>'
        '<li>Ask: <i>"What should I do when the payment gateway times out?"</i></li>'
        '<li>Upload a log or spec in the sidebar, then click a quick action above</li>'
        '</ul></div>',
        unsafe_allow_html=True,
    )


def login_hero():
    st.markdown(
        '<div class="login-hero"><div class="logo">📘</div><h1>Tech Doc Assistant</h1>'
        '<p>Sign in to ask questions about your technical documentation</p></div>',
        unsafe_allow_html=True,
    )


def user_badge(username, role):
    st.markdown(
        f'<div class="user-badge"><div class="avatar">{username[:1].upper()}</div>'
        f'<div><div class="uname">{username}</div><div class="role">{role}</div></div></div>',
        unsafe_allow_html=True,
    )


def admin_hero():
    st.markdown(
        '<div class="hero"><h1>Admin Panel</h1>'
        '<p>Manage the company knowledge base and the users of this app.</p></div>',
        unsafe_allow_html=True,
    )


def stat_cards(items):
    """items = [(number, label), ...]"""
    html = "".join(f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>' for n, l in items)
    st.markdown(f'<div class="stats">{html}</div>', unsafe_allow_html=True)
