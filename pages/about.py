import streamlit as st

st.set_page_config(
    page_title="How It Works — Dance Finder BCN",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --bg:      #07070f;
    --bg2:     #0d0d1a;
    --card:    rgba(13,13,26,0.9);
    --border:  rgba(255,255,255,0.07);
    --accent:  #6c4fff;
    --pink:    #ff4f9a;
    --blue:    #3d9bff;
    --green:   #3dffa0;
    --yellow:  #ffd700;
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

[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, [data-testid="collapsedControl"] { visibility: hidden; display: none; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 0 !important; max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important; }

.page-hero {
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    padding: 56px 64px 48px 64px;
    position: relative; overflow: hidden;
}
.page-hero::after {
    content: '⚙';
    position: absolute; right: 64px; top: 50%; transform: translateY(-50%);
    font-size: 10rem; opacity: 0.04; pointer-events: none;
}
.page-eyebrow { font-family: 'DM Sans', sans-serif; font-size: 0.62rem; font-weight: 600; letter-spacing: 5px; text-transform: uppercase; color: var(--pink); margin-bottom: 10px; }
.page-title   { font-family: 'Bebas Neue', sans-serif; font-size: 5rem; letter-spacing: 3px; color: var(--white); line-height: 0.9; margin: 0 0 12px 0; }
.page-title span { color: var(--accent); }
.page-sub     { font-family: 'DM Serif Display', serif; font-style: italic; font-size: 1.05rem; color: var(--muted); margin-bottom: 20px; }
.back-link    { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); text-decoration: none; }

.wrap { padding: 48px 64px; }

.sec-head { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 6px; color: var(--white); margin: 0 0 6px 0; }
.sec-line { width: 32px; height: 2px; background: var(--accent); border-radius: 2px; margin-bottom: 24px; }
.sec-desc { font-family: 'DM Sans', sans-serif; font-size: 0.84rem; color: var(--muted); margin-bottom: 24px; line-height: 1.7; }

.llm-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.llm-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 16px 0 0 16px;
}
.llm-card.gemini::before { background: #3d9bff; }
.llm-card.claude::before { background: #ff4f9a; }
.llm-card.cohere::before { background: #3dffa0; }

.llm-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'DM Sans', sans-serif; font-size: 0.62rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    padding: 4px 12px; border-radius: 100px; margin-bottom: 10px;
}
.llm-badge.gemini { background: rgba(61,155,255,0.1); color: #7ec3ff; border: 1px solid rgba(61,155,255,0.2); }
.llm-badge.claude { background: rgba(255,79,154,0.1); color: #ff9ac0; border: 1px solid rgba(255,79,154,0.2); }
.llm-badge.cohere { background: rgba(61,255,160,0.1); color: #3dffa0; border: 1px solid rgba(61,255,160,0.2); }

.llm-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 3px; color: var(--white); margin: 0 0 8px 0; }
.llm-desc  { font-family: 'DM Sans', sans-serif; font-size: 0.82rem; color: var(--text); line-height: 1.7; margin-bottom: 12px; }
.llm-why   { font-family: 'DM Sans', sans-serif; font-size: 0.76rem; color: var(--muted); background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; line-height: 1.6; }
.llm-why b { color: var(--text); }

.pipeline-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.pipe-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; letter-spacing: 4px; margin-bottom: 20px; }
.pipe-title.blue   { color: var(--blue); }
.pipe-title.purple { color: var(--accent); }

.pipe-step {
    display: flex; align-items: flex-start; gap: 16px;
    padding: 12px 0; border-bottom: 1px solid var(--border);
}
.pipe-step:last-child { border-bottom: none; }
.pipe-num {
    font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem;
    color: var(--accent); min-width: 28px; line-height: 1;
}
.pipe-content { flex: 1; }
.pipe-name { font-family: 'DM Sans', sans-serif; font-size: 0.82rem; font-weight: 600; color: var(--white); margin-bottom: 2px; }
.pipe-detail { font-family: 'DM Sans', sans-serif; font-size: 0.74rem; color: var(--muted); line-height: 1.5; }
.pipe-tag {
    font-family: 'DM Sans', sans-serif; font-size: 0.58rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 2px 8px; border-radius: 100px; margin-left: 6px;
    background: rgba(108,79,255,0.12); color: #b0a0ff;
    border: 1px solid rgba(108,79,255,0.2);
}

.feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 24px; }
.feature-card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px;
}
.feature-icon  { font-size: 1.4rem; margin-bottom: 8px; }
.feature-title { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; letter-spacing: 2px; color: var(--white); margin-bottom: 4px; }
.feature-desc  { font-family: 'DM Sans', sans-serif; font-size: 0.74rem; color: var(--muted); line-height: 1.5; }

.stack-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid var(--border);
    font-family: 'DM Sans', sans-serif; font-size: 0.78rem;
}
.stack-row:last-child { border-bottom: none; }
.stack-cat  { color: var(--muted); min-width: 140px; font-size: 0.68rem; letter-spacing: 1px; text-transform: uppercase; font-weight: 600; }
.stack-tool { color: var(--white); font-weight: 500; }
.stack-desc { color: var(--muted); font-size: 0.72rem; }

.crowd-box {
    background: rgba(108,79,255,0.06);
    border: 1px solid rgba(108,79,255,0.2);
    border-left: 3px solid var(--accent);
    border-radius: 0 12px 12px 12px;
    padding: 16px 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem; line-height: 1.7; color: var(--text);
    margin-bottom: 16px;
}
.crowd-title { font-size: 0.62rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: var(--accent); margin-bottom: 6px; }

.footer { background: var(--bg2); border-top: 1px solid var(--border); padding: 28px 64px; text-align: center; font-family: 'DM Sans', sans-serif; font-size: 0.68rem; color: var(--muted); letter-spacing: 1px; }

hr { border-color: var(--border) !important; margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── PAGE HERO ──
st.markdown("""
<div class="page-hero">
    <div class="page-eyebrow">PDAI Assignment 2 — How It Works</div>
    <h1 class="page-title">THE <span>PIPELINE</span></h1>
    <p class="page-sub">Three LLMs. Real data. One Barcelona dance discovery platform.</p>
    <a class="back-link" href="/" target="_self">← Back to Dance Finder</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="wrap">', unsafe_allow_html=True)

# ── SECTION 1: THE 3 PILLARS ──
st.markdown("""
<div class="sec-head">⚡ The 3 LLM Features</div>
<div class="sec-line"></div>
<p class="sec-desc">
    Dance Finder BCN uses three separate LLM APIs, each serving a distinct and non-trivial role in the pipeline.
    No LLM is used for a simple prompt → format response pattern.
</p>
""", unsafe_allow_html=True)

# Gemini
st.markdown("""
<div class="llm-card gemini">
    <div class="llm-badge gemini">🔵 LLM 1 — Gemini 1.5 Flash</div>
    <div class="llm-title">Web Scraper & Data Extractor</div>
    <div class="llm-desc">
        Gemini reads raw HTML scraped from real Barcelona dance studio websites and extracts structured class data.
        It handles missing fields, multilingual content (Spanish, Catalan, English), inconsistent layouts,
        and returns only valid JSON — no markdown, no explanation.
    </div>
    <div class="llm-why">
        <b>Why non-straightforward:</b> A simple prompt fails on real-world HTML.
        The final prompt went through 6+ iterations to handle edge cases.
        The JSON output is then post-processed by Python: validated, merged with
        studio metadata from studios.json, enriched with a heuristic crowd score,
        and written to classes.json — the LLM feeds the entire data pipeline.
    </div>
</div>
""", unsafe_allow_html=True)

# Claude / Gemini Chatbot
st.markdown("""
<div class="llm-card claude">
    <div class="llm-badge claude">🩷 LLM 2 — Gemini / Claude AI</div>
    <div class="llm-title">Natural Language Search & Multi-Turn Chatbot</div>
    <div class="llm-desc">
        Two separate API calls per user query. The first extracts structured filter parameters
        (style, level, free_only) from natural language and returns JSON that directly controls
        Streamlit widget state. The second provides a conversational answer using all current
        class data as RAG context, maintaining full multi-turn conversation history.
    </div>
    <div class="llm-why">
        <b>Why non-straightforward:</b> The LLM output from the first call is post-processed
        by Python to update five Streamlit filter dimensions simultaneously — the LLM directly
        drives UI state. The second call is a genuine RAG multi-turn chatbot, not a one-shot prompt.
    </div>
</div>
""", unsafe_allow_html=True)

# Cohere
st.markdown("""
<div class="llm-card cohere">
    <div class="llm-badge cohere">🟢 LLM 3 — Cohere Rerank</div>
    <div class="llm-title">Semantic Result Reranking</div>
    <div class="llm-desc">
        After the filters are applied, Cohere Rerank (rerank-english-v3.0) re-sorts the
        remaining classes by semantic relevance to the user's original query.
        A search for "latin vibes tonight" surfaces Salsa and Bachata above Ballet,
        even if all three pass the filters.
    </div>
    <div class="llm-why">
        <b>Why non-straightforward:</b> The LLM returns a ranked index list which Python
        uses to reorder the filtered classes array before passing it to the card renderer —
        the LLM directly controls the display order of the UI, decoupled from time_start sorting.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# ── SECTION 2: PIPELINE ──
st.markdown("""
<div class="sec-head">🔄 Data Pipeline</div>
<div class="sec-line"></div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="pipeline-wrap">
        <div class="pipe-title blue">OFFLINE PHASE — scraper.py</div>
        <div class="pipe-step">
            <div class="pipe-num">1</div>
            <div class="pipe-content">
                <div class="pipe-name">BeautifulSoup Scraper <span class="pipe-tag">Real</span></div>
                <div class="pipe-detail">Downloads HTML from 6 real Barcelona studio websites. Strips scripts, nav, footer — isolates content text.</div>
            </div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">2</div>
            <div class="pipe-content">
                <div class="pipe-name">Gemini Extraction <span class="pipe-tag">LLM 1</span></div>
                <div class="pipe-detail">Sends cleaned text to Gemini with a structured prompt. Returns JSON array of classes with all required fields.</div>
            </div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">3</div>
            <div class="pipe-content">
                <div class="pipe-name">Python Post-Processing</div>
                <div class="pipe-detail">Merges LLM output with studio metadata (GPS, links, Instagram). Adds heuristic crowd score. Saves to classes.json.</div>
            </div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">4</div>
            <div class="pipe-content">
                <div class="pipe-name">classes.json</div>
                <div class="pipe-detail">Structured output ready for runtime. 16 curated real classes from 6 Barcelona studios with verified URLs.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pipeline-wrap">
        <div class="pipe-title purple">RUNTIME PHASE — app.py</div>
        <div class="pipe-step">
            <div class="pipe-num">1</div>
            <div class="pipe-content">
                <div class="pipe-name">User Query</div>
                <div class="pipe-detail">User types natural language search: "Heels class tonight for beginners" or "free Salsa trial".</div>
            </div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">2</div>
            <div class="pipe-content">
                <div class="pipe-name">Claude / Gemini Filter Extraction <span class="pipe-tag">LLM 2</span></div>
                <div class="pipe-detail">First API call extracts filter parameters as JSON. Python applies them to all 5 Streamlit filter widgets.</div>
            </div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">3</div>
            <div class="pipe-content">
                <div class="pipe-name">Cohere Rerank <span class="pipe-tag">LLM 3</span></div>
                <div class="pipe-detail">Filtered results are semantically re-sorted by relevance to the original query before rendering.</div>
            </div>
        </div>
        <div class="pipe-step">
            <div class="pipe-num">4</div>
            <div class="pipe-content">
                <div class="pipe-name">Chatbot Response <span class="pipe-tag">LLM 2</span></div>
                <div class="pipe-detail">Second API call generates a conversational answer with studio details, times, prices and links.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# ── SECTION 3: CROWD SCORE ──
st.markdown("""
<div class="sec-head">📊 Crowd Score — How It Works</div>
<div class="sec-line"></div>
<div class="crowd-box">
    <div class="crowd-title">⚡ Heuristic Model — Rule-Based Estimation</div>
    The crowd score is calculated by a rule-based heuristic in database.py — not randomly assigned.
    It combines three signals: <b>weekday</b> (Friday = 1.0x, Monday = 0.7x),
    <b>time of day</b> (18:00–21:00 prime time = +0.15), and
    <b>style popularity</b> (Salsa base = 0.75, Tap base = 0.38).
    The result is displayed as a percentage bar on every card and map popup,
    clearly labelled as "estimated". In production, real user check-in data
    would replace this heuristic with a trained Random Forest model.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# ── SECTION 4: NON-LLM FEATURES ──
st.markdown("""
<div class="sec-head">✨ Non-LLM Improvements</div>
<div class="sec-line"></div>
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">⭐</div>
        <div class="feature-title">Community Ratings</div>
        <div class="feature-desc">Users rate classes 1–5 stars with optional comments. Stored in local SQLite database. Average shown live on every card.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📩</div>
        <div class="feature-title">Email Notifications</div>
        <div class="feature-desc">Register your email to subscribe to studios. Get alerted when new classes are added via Gmail SMTP (smtplib).</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📍</div>
        <div class="feature-title">Real Studio Data</div>
        <div class="feature-desc">17 real Barcelona studios with verified GPS, Instagram, Google Maps and website links. All clickable from every card.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎂</div>
        <div class="feature-title">Age Group Filter</div>
        <div class="feature-desc">New Kids (4–12) / Teens (13–17) / Adults (18+) filter added across all class cards and the filter bar.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🗺</div>
        <div class="feature-title">Enriched Map</div>
        <div class="feature-desc">Active classes shown as coloured markers (crowd level). All other studios shown as background markers with popup links.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎵</div>
        <div class="feature-title">20+ Dance Styles</div>
        <div class="feature-desc">Ballet, Flamenco, Voguing, Waacking, Tap, Heels, Dancehall, Afrobeats, Krump and more — fully filterable.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# ── SECTION 5: TECH STACK ──
st.markdown("""
<div class="sec-head">🛠 Tech Stack</div>
<div class="sec-line"></div>
""", unsafe_allow_html=True)

stack = [
    ("Frontend", "Streamlit", "Web app framework with custom CSS design system"),
    ("Map", "Folium + streamlit-folium", "Interactive dark-tile map with circle markers"),
    ("LLM 1", "Gemini 1.5 Flash", "Web scraping parser + chatbot fallback"),
    ("LLM 2", "Claude / Gemini AI", "Natural language search + multi-turn RAG chatbot"),
    ("LLM 3", "Cohere Rerank", "Semantic result reranking"),
    ("Web Scraping", "BeautifulSoup + requests", "Studio website HTML extraction"),
    ("Database", "SQLite (database.py)", "User ratings + email subscriptions"),
    ("Notifications", "smtplib + Gmail SMTP", "Email alerts for new classes"),
    ("Storage", "classes.json + studios.json", "Class data + curated studio metadata"),
    ("Deployment", "Streamlit Cloud", "Automatic deploy from GitHub on every push"),
    ("Version Control", "GitHub", "Public repository — no API keys committed"),
]

html = '<div class="pipeline-wrap">'
for cat, tool, desc in stack:
    html += (
        f'<div class="stack-row">'
        f'<span class="stack-cat">{cat}</span>'
        f'<span class="stack-tool">{tool}</span>'
        f'<span class="stack-desc"> — {desc}</span>'
        f'</div>'
    )
html += '</div>'
st.markdown(html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("---")
st.markdown("""
<div class="footer">
    <span style="font-family:'Bebas Neue',sans-serif;letter-spacing:3px;color:#f0f0ff;">
        DANCE<span style="color:#6c4fff;">FINDER</span> BCN
    </span>
    &nbsp;·&nbsp; PDAI Assignment 2 &nbsp;·&nbsp; Mara Rüsen &nbsp;·&nbsp; ESADE 2026
    &nbsp;·&nbsp; Gemini · Claude AI · Cohere · Streamlit · SQLite
</div>
""", unsafe_allow_html=True)
