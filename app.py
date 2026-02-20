import streamlit as st
import json
import folium
from streamlit_folium import st_folium
from datetime import date
import base64

st.set_page_config(
    page_title="Dance Finder",
    page_icon="🕺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');

    :root {
        --bg:     #080818;
        --bg2:    #0e0e28;
        --bg3:    #161635;
        --border: rgba(120, 100, 255, 0.18);
        --accent: #7c5cbf;
        --blue:   #4f8ef7;
        --glow:   rgba(100, 80, 220, 0.15);
        --text:   #c8c8e8;
        --muted:  #6a6a8a;
        --white:  #eeeeff;
    }

    /* ── BASE ── */
    .stApp {
        background-color: var(--bg);
        background-image:
            radial-gradient(ellipse at 15% 30%, rgba(70, 40, 180, 0.2) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 70%, rgba(30, 60, 180, 0.15) 0%, transparent 55%);
        color: var(--text);
    }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainMenu"] { display: none; }
    .block-container { padding-top: 0 !important; max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important; }

    /* ── HERO ── */
    .hero-wrapper {
        position: relative;
        width: 100%;
        height: 560px;
        overflow: hidden;
    }
    .hero-wrapper video {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        min-width: 100%; min-height: 100%;
        object-fit: cover;
        z-index: 0;
        opacity: 0.5;
    }
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            160deg,
            rgba(8,8,28,0.55) 0%,
            rgba(8,8,28,0.75) 60%,
            rgba(8,8,28,0.97) 100%
        );
        z-index: 1;
    }
    .hero-content {
        position: absolute;
        bottom: 60px;
        left: 56px;
        z-index: 2;
    }
    .hero-subtitle {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.6rem;
        letter-spacing: 10px;
        color: var(--blue);
        margin: 0;
        text-shadow: 0 0 40px rgba(79,142,247,0.6);
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 7rem;
        letter-spacing: 6px;
        color: var(--white);
        line-height: 0.88;
        margin: 0.1rem 0;
        text-shadow: 0 0 80px rgba(124,92,191,0.5);
    }
    .hero-location {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 4px;
        color: var(--muted);
        text-transform: uppercase;
        margin-top: 0.8rem;
    }
    .hero-btn {
        display: inline-block;
        margin-top: 1.1rem;
        padding: 9px 22px;
        border: 1px solid rgba(124,92,191,0.6);
        color: #a98ee0;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-decoration: none;
        border-radius: 4px;
        background: rgba(124,92,191,0.1);
        backdrop-filter: blur(6px);
        transition: all 0.25s ease;
    }
    .hero-btn:hover {
        background: rgba(124,92,191,0.3);
        color: #fff;
        border-color: rgba(124,92,191,0.9);
    }

    /* ── FILTER AREA ── */
    .filter-wrap {
        background: rgba(14,14,40,0.7);
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        backdrop-filter: blur(12px);
        padding: 0.8rem 1.5rem;
    }

    /* Override ALL Streamlit widget backgrounds to be dark+transparent */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="popover"] ul {
        background: rgba(20, 18, 50, 0.75) !important;
        border-color: rgba(120,100,255,0.2) !important;
        color: var(--text) !important;
    }
    /* Multiselect container */
    [data-testid="stMultiSelect"] > div > div {
        background: rgba(16, 14, 42, 0.8) !important;
        border-color: rgba(120,100,255,0.2) !important;
        backdrop-filter: blur(8px);
    }
    /* Multiselect TAGS — purple, not white */
    span[data-baseweb="tag"] {
        background: rgba(100, 75, 200, 0.3) !important;
        border: 1px solid rgba(120,100,255,0.35) !important;
        color: #c4b8ff !important;
    }
    span[data-baseweb="tag"] span { color: #c4b8ff !important; }
    /* Date input */
    [data-testid="stDateInput"] input {
        background: rgba(16, 14, 42, 0.8) !important;
        border-color: rgba(120,100,255,0.2) !important;
        color: var(--text) !important;
    }
    /* Labels */
    [data-testid="stMultiSelect"] label,
    [data-testid="stDateInput"] label,
    [data-testid="stToggle"] label {
        color: var(--muted) !important;
        font-size: 0.72rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    /* Toggle */
    [data-testid="stToggle"] p { color: var(--muted) !important; font-size: 0.75rem !important; }

    /* ── METRICS ── */
    [data-testid="stMetric"] {
        background: rgba(14, 12, 40, 0.5) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] p {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.7rem !important;
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 3rem !important;
        color: var(--white) !important;
        line-height: 1 !important;
    }

    /* ── TICKET CARDS ── */
    .ticket-card {
        background: rgba(14, 12, 42, 0.5);
        border: 1px solid var(--border);
        border-left: 3px solid rgba(124,92,191,0.7);
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.9rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .ticket-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 36px rgba(100,75,200,0.2);
        border-color: rgba(124,92,191,0.5);
    }
    .style-badge {
        display: inline-block;
        background: rgba(79,142,247,0.2);
        color: #90b8ff;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 0.82rem;
        letter-spacing: 2px;
        padding: 2px 10px;
        border-radius: 4px;
        margin-bottom: 0.3rem;
        border: 1px solid rgba(79,142,247,0.3);
    }
    .level-badge {
        display: inline-block;
        background: rgba(124,92,191,0.15);
        color: #a89de0;
        font-family: 'Inter', sans-serif;
        font-size: 0.66rem;
        letter-spacing: 1px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-left: 6px;
        text-transform: uppercase;
        border: 1px solid rgba(124,92,191,0.25);
    }
    .teacher-name {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.4rem;
        color: var(--white);
        letter-spacing: 2px;
        margin: 0.25rem 0 0.15rem 0;
    }
    .ticket-info {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        color: var(--muted);
        margin: 0.12rem 0;
    }
    .ticket-info span { color: var(--text); font-weight: 600; }
    .card-divider {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 0.6rem 0 !important;
    }
    .price-free {
        background: rgba(76,175,130,0.1); color: #6dcfaa;
        font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.78rem;
        padding: 3px 10px; border-radius: 20px; border: 1px solid rgba(76,175,130,0.3);
        display: inline-block;
    }
    .price-paid {
        background: rgba(180,160,255,0.1); color: #b4a0ff;
        font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.78rem;
        padding: 3px 10px; border-radius: 20px; border: 1px solid rgba(180,160,255,0.3);
        display: inline-block;
    }
    .crowd-hot {
        background: rgba(255,140,80,0.1); color: #ffaa60; font-size: 0.7rem;
        padding: 2px 8px; border-radius: 20px; border: 1px solid rgba(255,140,80,0.3);
        display: inline-block; margin-left: 8px;
    }
    .crowd-ok {
        background: rgba(90,180,214,0.1); color: #7ac8e8; font-size: 0.7rem;
        padding: 2px 8px; border-radius: 20px; border: 1px solid rgba(90,180,214,0.25);
        display: inline-block; margin-left: 8px;
    }

    /* ── SECTION HEADERS ── */
    .section-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 4px;
        color: var(--muted);
        text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
    }

    /* ── DIVIDERS ── */
    hr { border-color: var(--border) !important; margin: 0.6rem 0 !important; }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] {
        background: rgba(14,12,40,0.4) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpander"] summary { color: var(--muted) !important; }

    /* main content padding */
    .main-content { padding: 0 2rem; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_classes():
    with open("classes.json", "r") as f:
        return json.load(f)

classes = load_classes()

# ── VIDEO: load as base64 so it always works ──
@st.cache_data
def load_video_b64():
    try:
        with open("static/dance.mov", "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode("utf-8")
    except:
        return None

video_b64 = load_video_b64()
video_tag = ""
if video_b64:
    video_tag = f'<source src="data:video/mp4;base64,{video_b64}" type="video/mp4">'

# ── HERO ──
today = date.today()
location_str = f"Barcelona · {today.strftime('%A, %d %B %Y')}"

st.markdown(f"""
<div class="hero-wrapper">
    <video autoplay muted loop playsinline>
        {video_tag}
    </video>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-subtitle">DANCE CLASSES</div>
        <div class="hero-title">DANCE<br>FINDER</div>
        <div class="hero-location">📍 {location_str}</div>
        <a class="hero-btn" href="/about" target="_self">⚙ How it works →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FILTER BAR ──
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown("---")
f1, f2, f3, f4, f5 = st.columns([1.2, 1.5, 1.5, 1.5, 1])
with f1:
    selected_date = st.date_input("Date", value=date.today(), label_visibility="visible")
with f2:
    all_styles = sorted(set(c["style"] for c in classes))
    selected_styles = st.multiselect("Style", options=all_styles, default=all_styles, placeholder="All styles")
with f3:
    all_teachers = sorted(set(c["teacher"]["name"] for c in classes))
    selected_teachers = st.multiselect("Teacher", options=all_teachers, default=all_teachers, placeholder="All teachers")
with f4:
    all_levels = ["Beginner", "Intermediate", "Advanced", "All Levels"]
    selected_levels = st.multiselect("Level", options=all_levels, default=all_levels, placeholder="All levels")
with f5:
    free_only = st.toggle("Free only 🎁", value=False)

st.markdown("---")

# ── FILTER LOGIC ──
filtered = [
    c for c in classes
    if c["style"] in (selected_styles or all_styles)
    and c["teacher"]["name"] in (selected_teachers or all_teachers)
    and c["level"] in (selected_levels or all_levels)
    and (not free_only or c["free_trial"])
]
filtered = sorted(filtered, key=lambda x: x["time_start"])

# ── METRICS ──
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("🕺 Classes Today", len(filtered))
with m2:
    st.metric("🎁 Free Trials", sum(1 for c in filtered if c["free_trial"]))
with m3:
    st.metric("⚡ Selling Fast", sum(1 for c in filtered if c["crowd_score"] >= 0.8))
with m4:
    st.metric("🎵 Styles Available", len(set(c["style"] for c in filtered)))

st.markdown("---")

# ── MAP + CARDS ──
map_col, cards_col = st.columns([1, 1], gap="large")

with map_col:
    st.markdown('<div class="section-header">📍 Studios on the Map</div>', unsafe_allow_html=True)
    if filtered:
        avg_lat = sum(c["lat"] for c in filtered) / len(filtered)
        avg_lon = sum(c["lon"] for c in filtered) / len(filtered)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=14, tiles="CartoDB dark_matter")
        for c in filtered:
            color = "#ff8c50" if c["crowd_score"] >= 0.8 else "#a07cdf" if c["crowd_score"] >= 0.55 else "#4f8ef7"
            popup_html = f"""
            <div style="font-family:sans-serif;min-width:160px;background:#0e0e28;color:#c8c8e8;padding:8px;border-radius:6px;">
                <b style="color:#90b8ff;">{c['style']}</b><br>
                <b>{c['studio']}</b><br>
                🕐 {c['time_start']} – {c['time_end']}<br>
                👤 {c['teacher']['name']}<br>
                💶 {c['price_label']}
            </div>"""
            folium.CircleMarker(
                location=[c["lat"], c["lon"]],
                radius=10, color=color, fill=True,
                fill_color=color, fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=f"{c['style']} · {c['studio']}"
            ).add_to(m)
        st_folium(m, width=None, height=480, returned_objects=[])
        st.markdown('<div style="font-family:Inter;font-size:0.7rem;color:#555;margin-top:0.3rem;">🔵 Available &nbsp; 🟣 Filling Up &nbsp; 🟠 Almost Full</div>', unsafe_allow_html=True)
    else:
        st.info("No classes match your filters.")

with cards_col:
    st.markdown('<div class="section-header">🎫 Today\'s Classes</div>', unsafe_allow_html=True)
    if not filtered:
        st.warning("No classes found. Try changing your filters.")
    else:
        for c in filtered:
            score = c["crowd_score"]
            crowd_html = (
                f'<span class="crowd-hot">⚡ {int(score*100)}% Full</span>' if score >= 0.8
                else f'<span class="crowd-hot">🔥 {int(score*100)}% Full</span>' if score >= 0.55
                else f'<span class="crowd-ok">✅ {int(score*100)}% Full</span>'
            )
            price_html = (
                f'<span class="price-free">🎁 {c["price_label"]}</span>' if c["free_trial"]
                else f'<span class="price-paid">💜 {c["price_label"]}</span>'
            )
            neighborhood = c["address"].split(",")[1].strip() if "," in c["address"] else "Barcelona"

            st.markdown(f"""
            <div class="ticket-card">
                <span class="style-badge">{c['style']}</span>
                <span class="level-badge">{c['level']}</span>
                {crowd_html}
                <div class="teacher-name">{c['teacher']['name']}</div>
                <div class="ticket-info">📍 <span>{c['studio']}</span> · {neighborhood}</div>
                <div class="ticket-info">⏰ <span>{c['time_start']} – {c['time_end']}</span></div>
                <div class="ticket-info">🌍 <span>{c['teacher']['origin']}</span></div>
                <hr class="card-divider">
                {price_html}
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"ℹ️ About {c['teacher']['name']} + Today's Topic"):
                bio_col, topic_col = st.columns([2, 1])
                with bio_col:
                    st.markdown(f"**Origin:** {c['teacher']['origin']}")
                    st.markdown(f"**Instagram:** {c['teacher']['instagram']}")
                    st.markdown(f"**Styles:** {', '.join(c['teacher']['styles'])}")
                    st.markdown(f"**Bio:** {c['teacher']['bio']}")
                with topic_col:
                    st.info(f"🎯 **Today's Topic:**\n\n{c['teacher']['todays_topic']}")
                    st.markdown(f"[📅 Book Now →]({c['booking_link']})")

            with st.expander("📸 View Original Instagram Story (AI Source)"):
                st.markdown("""
                <div style="background:rgba(14,12,40,0.6);border:1px solid rgba(120,100,255,0.2);border-radius:10px;padding:1.2rem;text-align:center;font-family:Inter;color:#6a6a8a;font-size:0.82rem;backdrop-filter:blur(8px);">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">📱</div>
                    <b style="color:#c8c8e8;">Instagram Story Screenshot</b><br>
                    Original source the Vision LLM extracted data from.<br>
                    <span style="color:#a89de0;font-size:0.73rem;">Extracted: time · teacher · style · price · level</span>
                </div>
                """, unsafe_allow_html=True)
                st.caption("🤖 AI Confidence: High · Last updated: Today 06:00 AM")

st.markdown('</div>', unsafe_allow_html=True)
