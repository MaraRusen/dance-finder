from reranker import rerank_classes
import streamlit as st
import json
import folium
from streamlit_folium import st_folium
from datetime import date, datetime
import base64
import os
from dotenv import load_dotenv
from database import (
    init_db, add_user, user_exists, add_rating, get_studio_rating,
    subscribe_to_studio, get_user_subscriptions, estimate_crowd_score
)
from chatbot import chat, get_filter_instructions
from scraper import run_scraper

load_dotenv()
init_db()

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dance Finder BCN",
    page_icon="🕺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --bg:      #07070f;
    --bg2:     #0d0d1a;
    --bg3:     #121224;
    --card:    rgba(13,13,26,0.9);
    --border:  rgba(255,255,255,0.07);
    --accent:  #6c4fff;
    --pink:    #ff4f9a;
    --blue:    #3d9bff;
    --green:   #3dffa0;
    --text:    #d4d4e8;
    --muted:   #5a5a7a;
    --white:   #f0f0ff;
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(108,79,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(255,79,154,0.08) 0%, transparent 60%);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"]        { display: none !important; }
#MainMenu                        { visibility: hidden; }
footer                           { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
[data-testid="stHeader"]         { background: transparent; }
.block-container {
    padding-top: 0 !important;
    max-width: 100% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* NAVBAR */
.navbar {
    position: sticky; top: 0; z-index: 100;
    background: rgba(7,7,15,0.95); backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 0 64px; display: flex; align-items: center;
    justify-content: space-between; height: 56px;
}
.navbar-brand { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 3px; color: var(--white); }
.navbar-brand span { color: var(--accent); }
.navbar-right { display: flex; gap: 32px; align-items: center; }
.navbar-link  { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); text-decoration: none; }
.navbar-dot   { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); display: inline-block; margin-right: 6px; }

/* HERO */
.hero { position: relative; width: 100%; height: 620px; overflow: hidden; }
.hero video {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    min-width: 100%; min-height: 100%; object-fit: cover;
    opacity: 0.35; filter: hue-rotate(220deg) saturate(1.4); z-index: 0;
}
.hero-overlay {
    position: absolute; inset: 0; z-index: 1;
    background: linear-gradient(to bottom, rgba(7,7,15,0.3) 0%, rgba(7,7,15,0.6) 50%, rgba(7,7,15,0.98) 100%);
}
.hero-content { position: absolute; z-index: 2; bottom: 72px; left: 64px; }
.hero-kicker  { font-family: 'DM Sans', sans-serif; font-size: 0.65rem; font-weight: 500; letter-spacing: 5px; text-transform: uppercase; color: var(--pink); margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.hero-kicker::before { content: ''; display: inline-block; width: 24px; height: 1px; background: var(--pink); }
.hero-title   { font-family: 'Bebas Neue', sans-serif; font-size: 9rem; line-height: 0.88; letter-spacing: 2px; color: var(--white); text-shadow: 0 0 120px rgba(108,79,255,0.4); margin: 0; }
.hero-title span { color: var(--accent); }
.hero-sub     { font-family: 'DM Serif Display', serif; font-style: italic; font-size: 1.1rem; color: var(--muted); margin-top: 12px; }
.hero-pills   { display: flex; gap: 8px; margin-top: 20px; flex-wrap: wrap; }
.hero-pill    { font-family: 'DM Sans', sans-serif; font-size: 0.62rem; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; border: 1px solid rgba(108,79,255,0.4); color: #a89dff; background: rgba(108,79,255,0.08); }
.hero-cta     { display: inline-block; margin-top: 24px; padding: 11px 28px; background: var(--accent); color: #fff; font-family: 'DM Sans', sans-serif; font-size: 0.72rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; text-decoration: none; border-radius: 6px; margin-right: 12px; }
.hero-ghost   { display: inline-block; margin-top: 24px; padding: 10px 28px; border: 1px solid var(--border); color: var(--muted); font-family: 'DM Sans', sans-serif; font-size: 0.72rem; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; text-decoration: none; border-radius: 6px; }

/* AI SECTION */
.ai-section { background: var(--bg2); border-bottom: 1px solid var(--border); padding: 36px 64px; }
.ai-eyebrow { font-family: 'DM Sans', sans-serif; font-size: 0.62rem; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; color: var(--pink); margin-bottom: 6px; }
.ai-title   { font-family: 'Bebas Neue', sans-serif; font-size: 2.4rem; letter-spacing: 4px; color: var(--white); margin: 0 0 4px 0; }
.ai-desc    { font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: var(--muted); margin-bottom: 0; }

/* AI RESPONSE */
.ai-resp {
    background: rgba(108,79,255,0.06); border: 1px solid rgba(108,79,255,0.2);
    border-left: 3px solid var(--accent); border-radius: 0 12px 12px 12px;
    padding: 14px 18px; font-family: 'DM Sans', sans-serif; font-size: 0.84rem;
    line-height: 1.7; color: var(--text); margin-top: 10px;
}
.ai-resp-head { font-size: 0.6rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: var(--accent); margin-bottom: 6px; }
.ai-filter-notice { background: rgba(255,79,154,0.06); border: 1px solid rgba(255,79,154,0.2); border-radius: 8px; padding: 7px 14px; font-size: 0.72rem; color: #ff9ac0; margin-bottom: 10px; }

/* WIDGET OVERRIDES */
div[data-baseweb="input"] input, div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important; border-color: var(--border) !important; color: var(--text) !important;
}
[data-testid="stMultiSelect"] > div > div { background: rgba(255,255,255,0.04) !important; border-color: var(--border) !important; }
span[data-baseweb="tag"] { background: rgba(108,79,255,0.2) !important; border: 1px solid rgba(108,79,255,0.3) !important; color: #c4b8ff !important; }
[data-testid="stMultiSelect"] label, [data-testid="stDateInput"] label, [data-testid="stToggle"] label {
    color: var(--muted) !important; font-size: 0.64rem !important; letter-spacing: 2px; text-transform: uppercase; font-weight: 600 !important;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important; border-color: var(--border) !important;
    color: var(--white) !important; font-size: 0.9rem !important; border-radius: 8px !important;
}
[data-testid="stTextInput"] input:focus { border-color: rgba(108,79,255,0.5) !important; box-shadow: 0 0 0 3px rgba(108,79,255,0.12) !important; }
[data-testid="stTextInput"] label { color: var(--muted) !important; font-size: 0.64rem !important; letter-spacing: 2px; text-transform: uppercase; font-weight: 600 !important; }
[data-testid="stToggle"] p { color: var(--muted) !important; font-size: 0.74rem !important; }
[data-testid="stDateInput"] input { background: rgba(255,255,255,0.04) !important; border-color: var(--border) !important; color: var(--text) !important; }

/* METRICS */
[data-testid="stMetric"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px; padding: 20px 24px !important; }
[data-testid="stMetricLabel"] p { font-family: 'DM Sans', sans-serif !important; font-size: 0.62rem !important; font-weight: 600 !important; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 2px; }
[data-testid="stMetricValue"] { font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; color: var(--white) !important; line-height: 1 !important; }

/* SECTION HEADER */
.sec-head { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 6px; color: var(--white); margin: 0 0 6px 0; }
.sec-line { width: 32px; height: 2px; background: var(--accent); border-radius: 2px; margin-bottom: 20px; }

/* TICKET CARDS */
.ticket {
    background: var(--card); border: 1px solid var(--border); border-radius: 16px;
    padding: 20px 24px; margin-bottom: 14px; position: relative; overflow: hidden;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
}
.ticket::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: var(--accent); border-radius: 16px 0 0 16px; }
.ticket:hover { transform: translateY(-2px); border-color: rgba(108,79,255,0.3); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
.t-top   { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.t-badges { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.badge { font-family: 'DM Sans', sans-serif; font-size: 0.6rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 3px 9px; border-radius: 100px; }
.b-style { background: rgba(61,155,255,0.12); color: #7ec3ff; border: 1px solid rgba(61,155,255,0.2); }
.b-level { background: rgba(108,79,255,0.1); color: #b0a0ff; border: 1px solid rgba(108,79,255,0.2); }
.b-age   { background: rgba(255,79,154,0.08); color: #ff9ac0; border: 1px solid rgba(255,79,154,0.15); }
.b-free  { background: rgba(61,255,160,0.08); color: #3dffa0; border: 1px solid rgba(61,255,160,0.2); }
.crowd-wrap { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; min-width: 76px; }
.crowd-lbl { font-family: 'DM Sans', sans-serif; font-size: 0.58rem; font-weight: 600; letter-spacing: 1px; color: var(--muted); text-transform: uppercase; }
.crowd-pct { font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; line-height: 1; }
.c-hot { color: #ff7050; } .c-mid { color: #ffb040; } .c-ok { color: #3dffa0; }
.crowd-bar  { width: 76px; height: 3px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
.crowd-fill { height: 100%; border-radius: 2px; }
.t-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.65rem; letter-spacing: 2px; color: var(--white); line-height: 1; margin: 8px 0 5px 0; }
.t-meta { font-family: 'DM Sans', sans-serif; font-size: 0.76rem; color: var(--muted); display: flex; flex-direction: column; gap: 3px; }
.t-meta b { color: var(--text); font-weight: 500; }
.t-div  { border: none !important; border-top: 1px solid var(--border) !important; margin: 10px 0 !important; }
.t-bot  { display: flex; justify-content: space-between; align-items: center; }
.price-free { background: rgba(61,255,160,0.08); color: #3dffa0; border: 1px solid rgba(61,255,160,0.2); font-family: 'DM Sans', sans-serif; font-size: 0.76rem; font-weight: 600; padding: 4px 12px; border-radius: 100px; }
.price-paid { background: rgba(108,79,255,0.1); color: #b0a0ff; border: 1px solid rgba(108,79,255,0.2); font-family: 'DM Sans', sans-serif; font-size: 0.76rem; font-weight: 600; padding: 4px 12px; border-radius: 100px; }
.stars { color: #ffd700; font-size: 0.82rem; }
.rcount { font-family: 'DM Sans', sans-serif; font-size: 0.66rem; color: var(--muted); margin-left: 3px; }
.card-links { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
.cl { font-family: 'DM Sans', sans-serif; font-size: 0.6rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; padding: 4px 10px; border-radius: 6px; text-decoration: none; transition: all 0.15s; }
.cl-ig  { background: rgba(255,79,154,0.08); color: #ff9ac0; border: 1px solid rgba(255,79,154,0.15); }
.cl-ig:hover  { background: rgba(255,79,154,0.2); color: #fff; }
.cl-map { background: rgba(61,155,255,0.08); color: #7ec3ff; border: 1px solid rgba(61,155,255,0.15); }
.cl-map:hover { background: rgba(61,155,255,0.2); color: #fff; }
.cl-web { background: rgba(108,79,255,0.08); color: #b0a0ff; border: 1px solid rgba(108,79,255,0.15); }
.cl-web:hover { background: rgba(108,79,255,0.2); color: #fff; }

/* CHATBOT */
.chat-u { background: rgba(108,79,255,0.1); border: 1px solid rgba(108,79,255,0.2); border-radius: 16px 16px 4px 16px; padding: 10px 15px; font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: #c4b8ff; max-width: 75%; float: right; clear: both; margin-bottom: 8px; }
.chat-a { background: var(--card); border: 1px solid var(--border); border-radius: 16px 16px 16px 4px; padding: 12px 15px; font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: var(--text); line-height: 1.65; max-width: 80%; float: left; clear: both; margin-bottom: 12px; }
.chat-lbl { font-family: 'DM Sans', sans-serif; font-size: 0.58rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: 3px; }
.chat-scroll { max-height: 360px; overflow-y: auto; padding: 4px; margin-bottom: 12px; scrollbar-width: thin; scrollbar-color: rgba(108,79,255,0.3) transparent; }

/* PANELS */
.panel { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 20px 22px; }
.panel-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.05rem; letter-spacing: 4px; color: var(--white); margin-bottom: 4px; }
.panel-desc  { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; color: var(--muted); margin-bottom: 14px; }
.pipe-box    { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 18px 22px; margin-top: 14px; }
.pipe-title  { font-family: 'Bebas Neue', sans-serif; font-size: 0.95rem; letter-spacing: 4px; color: var(--blue); margin-bottom: 8px; }
.pipe-step   { font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: var(--muted); padding: 5px 0; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 8px; }
.pipe-step:last-child { border-bottom: none; }
.pipe-num    { font-family: 'Bebas Neue', sans-serif; font-size: 0.9rem; color: var(--accent); min-width: 16px; }
.scraper-ok  { background: rgba(61,155,255,0.06); border: 1px solid rgba(61,155,255,0.15); border-radius: 8px; padding: 7px 12px; font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: #7ec3ff; margin-top: 8px; }
.notif-badge { display: inline-block; background: rgba(61,255,160,0.1); border: 1px solid rgba(61,255,160,0.2); color: #3dffa0; font-family: 'DM Sans', sans-serif; font-size: 0.6rem; font-weight: 600; letter-spacing: 1px; padding: 3px 8px; border-radius: 100px; margin: 2px; }

/* BUTTONS */
[data-testid="stButton"] button { background: rgba(108,79,255,0.12) !important; border: 1px solid rgba(108,79,255,0.3) !important; color: #c4b8ff !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 2px !important; text-transform: uppercase !important; border-radius: 8px !important; }
[data-testid="stButton"] button:hover { background: rgba(108,79,255,0.25) !important; border-color: rgba(108,79,255,0.6) !important; color: #fff !important; }

/* EXPANDERS */
[data-testid="stExpander"] { background: rgba(255,255,255,0.02) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
[data-testid="stExpander"] summary { color: var(--muted) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.74rem !important; font-weight: 500 !important; }

/* MISC */
hr { border-color: var(--border) !important; margin: 0 !important; }
.wrap  { padding: 0 64px 48px 64px; }
.empty { text-align: center; padding: 60px 32px; font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 4px; color: var(--muted); }
.footer { background: var(--bg2); border-top: 1px solid var(--border); padding: 28px 64px; text-align: center; font-family: 'DM Sans', sans-serif; font-size: 0.68rem; color: var(--muted); letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "conversation_history": [],
    "chat_display": [],
    "ai_response": None,
    "ai_filters": None,
    "scraper_status": None,
    "user_email": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# DATA LOADERS
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_classes():
    try:
        with open("classes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for c in data:
            if not c.get("crowd_score"):
                c["crowd_score"] = estimate_crowd_score(
                    c.get("style", ""), c.get("time_start", "19:00")
                )
        return data
    except:
        return []

@st.cache_data
def load_studios():
    try:
        with open("studios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

@st.cache_data
def load_video_b64():
    try:
        with open("static/dance.mov", "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return None

classes   = load_classes()
studios   = load_studios()
video_b64 = load_video_b64()
video_tag = f'<source src="data:video/mp4;base64,{video_b64}" type="video/mp4">' if video_b64 else ""

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def render_stars(avg, count):
    if avg is None:
        return '<span style="font-family:DM Sans;font-size:0.66rem;color:#5a5a7a;">No ratings yet</span>'
    full  = int(avg)
    half  = 1 if (avg - full) >= 0.5 else 0
    empty = 5 - full - half
    s = "★" * full + ("½" if half else "") + "☆" * empty
    return f'<span class="stars">{s}</span><span class="rcount">({count})</span>'

def crowd_info(score):
    if score >= 0.75: return "c-hot", "#ff7050"
    if score >= 0.5:  return "c-mid", "#ffb040"
    return "c-ok", "#3dffa0"

def get_hood(c):
    addr = c.get("address", "")
    return addr.split(",")[1].strip() if "," in addr else "Barcelona"

# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────
today   = date.today()
day_str = today.strftime("%a %d %b %Y").upper()
st.markdown(f"""
<div class="navbar">
    <div class="navbar-brand">DANCE<span>FINDER</span> BCN</div>
    <div class="navbar-right">
        <span class="navbar-dot"></span>
        <span style="font-family:'DM Sans',sans-serif;font-size:0.62rem;letter-spacing:2px;text-transform:uppercase;color:#5a5a7a;">{day_str}</span>
        <a class="navbar-link" href="/about" target="_self">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <video autoplay muted loop playsinline>{video_tag}</video>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-kicker">AI-Powered Dance Discovery</div>
        <h1 class="hero-title">DANCE<br><span>FINDER</span></h1>
        <p class="hero-sub">Every class. Every studio. Barcelona — tonight.</p>
        <div class="hero-pills">
            <span class="hero-pill">🤖 Claude AI Search</span>
            <span class="hero-pill">🌐 Real Studio Data</span>
            <span class="hero-pill">📍 Live Locations</span>
            <span class="hero-pill">⭐ Community Ratings</span>
            <span class="hero-pill">📩 Email Alerts</span>
        </div>
        <a class="hero-cta" href="/about" target="_self">How it works →</a>
        <a class="hero-ghost" href="/about" target="_self">Pipeline</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AI SEARCH
# ─────────────────────────────────────────────
st.markdown("""
<div class="ai-section">
    <div class="ai-eyebrow">✦ Powered by Claude AI</div>
    <div class="ai-title">ASK ANYTHING</div>
    <div class="ai-desc">Search in natural language — Claude understands you and filters results in real time</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="wrap">', unsafe_allow_html=True)

sc1, sc2 = st.columns([5, 1])
with sc1:
    ai_query = st.text_input(
        "Search",
        placeholder='"Heels class tonight for beginners"  ·  "Salsa advanced Eixample"  ·  "free trial today"',
        label_visibility="collapsed",
        key="ai_search"
    )
with sc2:
    search_hit = st.button("🔍  Search", use_container_width=True)

if search_hit and ai_query and classes:
    with st.spinner("Claude is thinking..."):
        resp, hist = chat(ai_query, st.session_state.conversation_history.copy(), classes)
        st.session_state.conversation_history = hist
        st.session_state.ai_response  = resp
        st.session_state.ai_filters   = get_filter_instructions(ai_query, classes)
        st.session_state.chat_display.append({"user": ai_query, "ai": resp})

if st.session_state.ai_response:
    st.markdown(
        '<div class="ai-resp">'
        '<div class="ai-resp-head">🕺 Dance Finder AI</div>'
        + st.session_state.ai_response +
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("✕  Clear Search"):
        st.session_state.ai_response  = None
        st.session_state.ai_filters   = None
        st.session_state.conversation_history = []
        st.session_state.chat_display = []
        st.rerun()

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
ai_f = st.session_state.ai_filters or {}

ALL_STYLES = sorted(set(c.get("style","") for c in classes)) if classes else [
    "Afrobeats","Ballet","Bachata","Breaking","Commercial","Contemporary",
    "Dancehall","Flamenco","Heels","Hip Hop","House","Jazz","Krump",
    "Latin","Locking","Popping","Reggaeton","Salsa","Tap","Tango","Waacking","Voguing"
]
ALL_LEVELS = ["Beginner","Intermediate","Advanced","All Levels"]
ALL_AGES   = ["Kids (4–12)","Teens (13–17)","Adults (18+)"]
ALL_HOODS  = sorted(set(get_hood(c) for c in classes)) if classes else []

d_styles = [s for s in (ai_f.get("styles") or []) if s in ALL_STYLES] or ALL_STYLES
d_levels = [l for l in (ai_f.get("levels") or []) if l in ALL_LEVELS] or ALL_LEVELS
d_free   = ai_f.get("free_only", False)

if st.session_state.ai_filters and (len(d_styles) < len(ALL_STYLES) or d_free):
    st.markdown('<div class="ai-filter-notice">✦ AI filters applied — adjust manually below if needed</div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4, fc5, fc6 = st.columns([1, 1.6, 1.3, 1.3, 1.3, 0.8])
with fc1: sel_date   = st.date_input("Date", value=date.today())
with fc2: sel_styles = st.multiselect("Style", ALL_STYLES, default=d_styles, placeholder="All styles")
with fc3: sel_levels = st.multiselect("Level", ALL_LEVELS, default=d_levels, placeholder="All levels")
with fc4: sel_ages   = st.multiselect("Age Group", ALL_AGES, default=ALL_AGES, placeholder="All ages")
with fc5: sel_hoods  = st.multiselect("Neighborhood", ALL_HOODS, placeholder="All areas")
with fc6: free_only  = st.toggle("Free 🎁", value=d_free)

st.markdown("---")

# ─────────────────────────────────────────────
# FILTER LOGIC
# ─────────────────────────────────────────────
filtered = [
    c for c in classes
    if c.get("style") in (sel_styles or ALL_STYLES)
    and c.get("level") in (sel_levels or ALL_LEVELS)
    and (not free_only or c.get("free_trial", False))
    and (not sel_hoods or get_hood(c) in sel_hoods)
]
filtered = sorted(filtered, key=lambda x: x.get("time_start", ""))

# Cohere reranking if AI search is active
if st.session_state.ai_response and ai_query:
    filtered = rerank_classes(ai_query, filtered)

# ─────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.metric("🕺  Classes", len(filtered))
with m2: st.metric("🎁  Free", sum(1 for c in filtered if c.get("free_trial")))
with m3: st.metric("⚡  Selling Fast", sum(1 for c in filtered if c.get("crowd_score", 0) >= 0.75))
with m4: st.metric("🎵  Styles", len(set(c.get("style") for c in filtered)))
with m5: st.metric("🏢  Studios", len(set(c.get("studio") for c in filtered)))

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAP + CARDS
# ─────────────────────────────────────────────
map_col, cards_col = st.columns([1, 1], gap="large")

# ── MAP ──
with map_col:
    st.markdown('<div class="sec-head">📍 Studios on the Map</div><div class="sec-line"></div>', unsafe_allow_html=True)
    if filtered:
        avg_lat = sum(c.get("lat", 41.3851) for c in filtered) / len(filtered)
        avg_lon = sum(c.get("lon", 2.1734)  for c in filtered) / len(filtered)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=14, tiles="CartoDB dark_matter")
        for c in filtered:
            score = c.get("crowd_score", 0.5)
            _, bar_color = crowd_info(score)
            r_data = get_studio_rating(c.get("studio", ""))
            rating_str = f"⭐ {r_data['average']}/5 ({r_data['count']})" if r_data["average"] else "No ratings yet"
            maps_link  = c.get("maps_link", "")
            maps_btn   = f'<a href="{maps_link}" target="_blank" style="display:inline-block;margin-top:8px;padding:4px 10px;background:#3d9bff;color:#fff;border-radius:5px;font-size:0.72rem;text-decoration:none;">📍 Open in Maps</a>' if maps_link else ""
            popup_html = (
                '<div style="font-family:sans-serif;min-width:190px;background:#0d0d1a;color:#d4d4e8;'
                'padding:12px;border-radius:10px;border:1px solid rgba(255,255,255,0.08);">'
                f'<div style="color:#7ec3ff;font-weight:700;font-size:0.95rem;">{c.get("style","")}</div>'
                f'<div style="color:#f0f0ff;font-weight:600;margin:2px 0 6px 0;">{c.get("studio","")}</div>'
                f'<div style="font-size:0.76rem;">⏰ {c.get("time_start","?")} – {c.get("time_end","?")}</div>'
                f'<div style="font-size:0.76rem;">👤 {c.get("teacher",{}).get("name","")}</div>'
                f'<div style="font-size:0.76rem;">💶 {c.get("price_label","")}</div>'
                f'<div style="font-size:0.76rem;color:{bar_color};">⚡ {int(score*100)}% Full</div>'
                f'<div style="font-size:0.7rem;color:#ffd700;margin-top:4px;">{rating_str}</div>'
                f'{maps_btn}'
                '</div>'
            )
            folium.CircleMarker(
                location=[c.get("lat", avg_lat), c.get("lon", avg_lon)],
                radius=12, color=bar_color, fill=True,
                fill_color=bar_color, fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=230),
                tooltip=f"{c.get('style','')} · {c.get('studio','')} · {int(score*100)}% full"
            ).add_to(m)
            #############################
        # Add all studios as background markers
# All studios as background markers
        shown_coords = [(c.get("lat"), c.get("lon")) for c in filtered]
        for s in studios:
            if (s["lat"], s["lon"]) not in shown_coords:
                folium.CircleMarker(
                    location=[s["lat"], s["lon"]],
                    radius=7,
                    color="#3a3a6a",
                    fill=True,
                    fill_color="#2a2a4a",
                    fill_opacity=0.7,
                    tooltip=f"📍 {s['name']}",
                    popup=folium.Popup(
                        f'<div style="font-family:sans-serif;background:#0d0d1a;color:#d4d4e8;padding:10px;border-radius:8px;">'
                        f'<b style="color:#7ec3ff;">{s["name"]}</b><br>'
                        f'<a href="{s.get("url","")}" target="_blank" style="color:#b0a0ff;font-size:0.72rem;">🌐 Website</a></div>',
                        max_width=200
                    )
                ).add_to(m)

        st_folium(m, width=None, height=520, returned_objects=[])
                ##############################
        st.markdown(
            '<div style="font-family:DM Sans;font-size:0.63rem;color:#5a5a7a;margin-top:6px;letter-spacing:1px;">'
            '🟢 Available &nbsp;·&nbsp; 🟡 Filling Up &nbsp;·&nbsp; 🔴 Almost Full &nbsp;·&nbsp;'
            '<i>Crowd estimated via weekday · time · style heuristic</i></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="empty">No classes match your filters</div>', unsafe_allow_html=True)

# ── CARDS ──
with cards_col:
    st.markdown('<div class="sec-head">🎫 Today\'s Classes</div><div class="sec-line"></div>', unsafe_allow_html=True)
    if not filtered:
        st.markdown('<div class="empty">Try adjusting your filters</div>', unsafe_allow_html=True)
    else:
        for c in filtered:
            score   = c.get("crowd_score", 0.5)
            cc, bar_color = crowd_info(score)
            pct     = int(score * 100)
            teacher = c.get("teacher", {})
            hood    = get_hood(c)
            r_data  = get_studio_rating(c.get("studio", ""))
            stars_html = render_stars(r_data["average"], r_data["count"])
            age_group  = c.get("age_group", "Adults (18+)")

            # Price
            if c.get("free_trial"):
                price_html = f'<span class="price-free">🎁 {c.get("price_label","")}</span>'
            else:
                price_html = f'<span class="price-paid">💜 {c.get("price_label","")}</span>'

            # Free badge
            free_badge = '<span class="badge b-free">Free Trial</span>' if c.get("free_trial") else ""

            # Links
            links_html = ""
            if c.get("instagram_studio"):
                links_html += f'<a href="{c["instagram_studio"]}" target="_blank" class="cl cl-ig">📸 Instagram</a>'
            if c.get("maps_link"):
                links_html += f'<a href="{c["maps_link"]}" target="_blank" class="cl cl-map">📍 Maps</a>'
            if c.get("website"):
                links_html += f'<a href="{c["website"]}" target="_blank" class="cl cl-web">🌐 Website</a>'

            # Build card as concatenated string — avoids Streamlit HTML escaping
            card = (
                '<div class="ticket">'
                  '<div class="t-top">'
                    '<div class="t-badges">'
                      f'<span class="badge b-style">{c.get("style","")}</span>'
                      f'<span class="badge b-level">{c.get("level","")}</span>'
                      f'<span class="badge b-age">{age_group}</span>'
                      f'{free_badge}'
                    '</div>'
                    '<div class="crowd-wrap">'
                      '<span class="crowd-lbl">Crowd</span>'
                      f'<span class="crowd-pct {cc}">{pct}%</span>'
                      '<div class="crowd-bar">'
                        f'<div class="crowd-fill" style="width:{pct}%;background:{bar_color};"></div>'
                      '</div>'
                    '</div>'
                  '</div>'
                  f'<div class="t-name">{teacher.get("name","")}</div>'
                  '<div class="t-meta">'
                    f'<div>📍 <b>{c.get("studio","")}</b> · {hood}</div>'
                    f'<div>⏰ <b>{c.get("time_start","?")} – {c.get("time_end","?")}</b></div>'
                    f'<div>🌍 <b>{teacher.get("origin","")}</b></div>'
                  '</div>'
                  '<hr class="t-div">'
                  '<div class="t-bot">'
                    f'{price_html}'
                    f'<div>{stars_html}</div>'
                  '</div>'
                  f'<div class="card-links">{links_html}</div>'
                '</div>'
            )
            st.markdown(card, unsafe_allow_html=True)

            # Expander: Teacher bio
            with st.expander(f"ℹ️  About {teacher.get('name','')} · Today's Topic"):
                b1, b2 = st.columns([2, 1])
                with b1:
                    if teacher.get("origin"):    st.markdown(f"**Origin:** {teacher['origin']}")
                    if teacher.get("instagram"): st.markdown(f"**Instagram:** {teacher['instagram']}")
                    if teacher.get("styles"):    st.markdown(f"**Styles:** {', '.join(teacher['styles'])}")
                    if teacher.get("bio"):       st.markdown(f"**Bio:** {teacher['bio']}")
                with b2:
                    if teacher.get("todays_topic"):
                        st.info(f"🎯 **Today's Topic:**\n\n{teacher['todays_topic']}")
                    if c.get("booking_link"):
                        st.markdown(f"[📅 Book Now →]({c['booking_link']})")

            # Expander: Rate + Subscribe
            with st.expander(f"⭐  Rate & Subscribe — {c.get('studio','')}"):
                r1, r2 = st.columns(2)
                with r1:
                    st.markdown("**Rate this class**")
                    stars_sel = st.selectbox(
                        "Stars", [5, 4, 3, 2, 1],
                        format_func=lambda x: "★" * x + "☆" * (5 - x),
                        key=f"stars_{c.get('studio','')}_{c.get('time_start','')}"
                    )
                    comment_sel = st.text_input(
                        "Comment (optional)",
                        placeholder="Great energy!",
                        key=f"comment_{c.get('studio','')}_{c.get('time_start','')}"
                    )
                    if st.button("Submit Rating ⭐", key=f"rate_{c.get('studio','')}_{c.get('time_start','')}"):
                        res = add_rating(
                            studio_name=c.get("studio", ""),
                            stars=stars_sel,
                            user_email=st.session_state.user_email,
                            class_style=c.get("style", ""),
                            comment=comment_sel
                        )
                        st.success(res["message"])
                        load_classes.clear()
                        st.rerun()
                with r2:
                    st.markdown("**Get notified**")
                    if st.session_state.user_email:
                        subs = get_user_subscriptions(st.session_state.user_email)
                        if c.get("studio", "") in subs:
                            st.markdown('<span class="notif-badge">✓ Subscribed</span>', unsafe_allow_html=True)
                        else:
                            if st.button("🔔 Notify me", key=f"notif_{c.get('studio','')}_{c.get('time_start','')}"):
                                res2 = subscribe_to_studio(st.session_state.user_email, c.get("studio", ""))
                                st.success(res2["message"])
                    else:
                        st.caption("Register below to receive email notifications!")

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHATBOT + USER PANEL
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

chat_col, panel_col = st.columns([3, 2], gap="large")

with chat_col:
    st.markdown('<div class="sec-head">💬 Chat with Dance Finder AI</div><div class="sec-line"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:\'DM Sans\',sans-serif;font-size:0.76rem;color:#5a5a7a;margin-bottom:14px;">'
        'Multi-turn conversation — ask follow-ups, compare studios, get personalised recommendations.</p>',
        unsafe_allow_html=True
    )

    if st.session_state.chat_display:
        html = '<div class="chat-scroll">'
        for turn in st.session_state.chat_display:
            html += (
                '<div style="overflow:hidden;margin-bottom:5px;">'
                '<div class="chat-lbl" style="text-align:right;">You</div>'
                '<div style="display:flex;justify-content:flex-end;">'
                f'<div class="chat-u">{turn["user"]}</div>'
                '</div></div>'
                '<div style="overflow:hidden;margin-bottom:12px;">'
                '<div class="chat-lbl">🕺 Dance Finder AI</div>'
                f'<div class="chat-a">{turn["ai"]}</div>'
                '</div>'
            )
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    ci1, ci2 = st.columns([4, 1])
    with ci1:
        followup = st.text_input("Chat", placeholder="Ask a follow-up...", label_visibility="collapsed", key="chat_input")
    with ci2:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and followup and classes:
        with st.spinner("Thinking..."):
            resp, hist = chat(followup, st.session_state.conversation_history.copy(), classes)
            st.session_state.conversation_history = hist
            st.session_state.chat_display.append({"user": followup, "ai": resp})
            st.rerun()

    if st.session_state.chat_display:
        if st.button("🗑  Reset conversation"):
            st.session_state.conversation_history = []
            st.session_state.chat_display         = []
            st.session_state.ai_response          = None
            st.session_state.ai_filters           = None
            st.rerun()

with panel_col:
    # User registration
    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">📩 STAY IN THE LOOP</div>'
        '<div class="panel-desc">Register to rate classes and get email alerts when new ones drop</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if not st.session_state.user_email:
        email_in = st.text_input("Email", placeholder="your@email.com", label_visibility="collapsed", key="email_reg")
        if st.button("Register →  Get Alerts", use_container_width=True):
            if email_in and "@" in email_in:
                add_user(email_in)
                st.session_state.user_email = email_in
                st.success(f"✓ Welcome! {email_in}")
            else:
                st.error("Please enter a valid email address.")
    else:
        subs = get_user_subscriptions(st.session_state.user_email)
        st.markdown(
            f'<div style="font-family:DM Sans;font-size:0.76rem;color:#3dffa0;padding:6px 0;">'
            f'✓ {st.session_state.user_email}<br>'
            f'<span style="color:#5a5a7a;">Subscribed to {len(subs)} studio(s)</span></div>',
            unsafe_allow_html=True
        )
        for s in subs:
            st.markdown(f'<span class="notif-badge">🔔 {s}</span>', unsafe_allow_html=True)
        if st.button("Log out"):
            st.session_state.user_email = None
            st.rerun()

    # Pipeline box
    st.markdown(
        '<div class="pipe-box">'
        '<div class="pipe-title">⚙ DATA PIPELINE</div>'
        '<div class="pipe-step"><span class="pipe-num">1</span>Gemini scrapes real studio websites</div>'
        '<div class="pipe-step"><span class="pipe-num">2</span>Extracts classes → structured JSON</div>'
        '<div class="pipe-step"><span class="pipe-num">3</span>Crowd score via day + time + style heuristic</div>'
        '<div class="pipe-step"><span class="pipe-num">4</span>Claude AI answers natural language queries</div>'
        '<div class="pipe-step"><span class="pipe-num">5</span>Ratings + users stored in local SQLite DB</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🔄  Refresh Data via Gemini Scraper", use_container_width=True):
        with st.spinner("Gemini is scraping Barcelona studios..."):
            try:
                new_classes = run_scraper()
                n_studios   = len(set(c.get("studio") for c in new_classes))
                st.session_state.scraper_status = f"✅ {len(new_classes)} classes from {n_studios} studios"
                load_classes.clear()
                st.rerun()
            except Exception as e:
                st.session_state.scraper_status = f"⚠️ {str(e)}"

    if st.session_state.scraper_status:
        st.markdown(f'<div class="scraper-ok">{st.session_state.scraper_status}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f'<div class="footer">'
    f'<span style="font-family:\'Bebas Neue\',sans-serif;letter-spacing:3px;color:#f0f0ff;">'
    f'DANCE<span style="color:#6c4fff;">FINDER</span> BCN</span>'
    f' &nbsp;·&nbsp; ESADE 2026 &nbsp;·&nbsp; Mara Rüsen'
    f' &nbsp;·&nbsp; Streamlit · Gemini · Claude AI · SQLite'
    f' &nbsp;·&nbsp; {len(classes)} classes · {len(studios)} studios'
    f'</div>',
    unsafe_allow_html=True
)
