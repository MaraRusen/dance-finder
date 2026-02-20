import streamlit as st

st.set_page_config(
    page_title="How It Works · Dance Finder",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');

    :root {
        --bg:     #080818;
        --bg2:    #0e0e28;
        --border: rgba(120, 100, 255, 0.18);
        --accent: #7c5cbf;
        --blue:   #4f8ef7;
        --text:   #c8c8e8;
        --muted:  #6a6a8a;
        --white:  #eeeeff;
    }

    .stApp {
        background-color: var(--bg);
        background-image:
            radial-gradient(ellipse at 15% 30%, rgba(70,40,180,0.2) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 70%, rgba(30,60,180,0.15) 0%, transparent 55%);
        color: var(--text);
    }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainMenu"] { display: none; }
    .block-container { padding-top: 3rem !important; max-width: 1100px !important; }

    .page-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 5rem;
        letter-spacing: 6px;
        color: var(--white);
        line-height: 0.9;
        margin: 0;
        text-shadow: 0 0 80px rgba(124,92,191,0.4);
    }
    .page-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 4px;
        color: var(--blue);
        text-transform: uppercase;
        margin-bottom: 2.5rem;
        margin-top: 0.4rem;
    }
    .section-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.6rem;
        letter-spacing: 4px;
        color: var(--blue);
        margin-top: 2.5rem;
        margin-bottom: 0.8rem;
    }

    /* Pillar cards */
    .pillar-card {
        background: rgba(14,12,42,0.55);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0,0,0,0.3);
        height: 100%;
    }
    .pillar-card h3 {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 2px;
        color: var(--white);
        margin: 0 0 0.6rem 0;
    }
    .pillar-card p {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: var(--muted);
        line-height: 1.7;
        margin: 0;
    }
    .pillar-accent { color: var(--blue); }

    /* Pipeline boxes */
    .pipe-box {
        background: rgba(14,12,42,0.5);
        border: 1px solid var(--border);
        border-left: 3px solid rgba(124,92,191,0.6);
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        backdrop-filter: blur(8px);
        font-family: 'Inter', sans-serif;
    }
    .pipe-box .tag {
        display: inline-block;
        background: rgba(79,142,247,0.15);
        color: #90b8ff;
        font-size: 0.65rem;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
        border: 1px solid rgba(79,142,247,0.25);
        margin-bottom: 0.5rem;
    }
    .pipe-box h4 {
        color: var(--white);
        font-size: 0.92rem;
        margin: 0 0 0.35rem 0;
        letter-spacing: 0.5px;
    }
    .pipe-box p {
        color: var(--muted);
        font-size: 0.8rem;
        margin: 0;
        line-height: 1.6;
    }
    .pipe-box code {
        background: rgba(124,92,191,0.15);
        color: #c4b8ff;
        padding: 1px 5px;
        border-radius: 3px;
        font-size: 0.75rem;
    }
    .arrow {
        text-align: center;
        font-size: 1.3rem;
        color: rgba(124,92,191,0.5);
        padding-top: 2.2rem;
    }

    /* Tech stack */
    .tech-col h4 {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1rem;
        letter-spacing: 2px;
        color: var(--blue);
        margin-bottom: 0.5rem;
    }
    .tech-col p, .tech-col li {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: var(--muted);
        line-height: 1.8;
    }

    hr { border-color: var(--border) !important; }

    /* Back button */
    .back-btn {
        display: inline-block;
        margin-bottom: 2rem;
        padding: 8px 18px;
        border: 1px solid var(--border);
        color: var(--muted);
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-decoration: none;
        border-radius: 4px;
        background: rgba(124,92,191,0.07);
        backdrop-filter: blur(4px);
        transition: all 0.2s ease;
    }
    .back-btn:hover { color: var(--white); border-color: rgba(124,92,191,0.5); }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown('<a class="back-btn" href="/" target="_self">← Back to Dance Finder</a>', unsafe_allow_html=True)
st.markdown('<div class="page-title">HOW IT<br>WORKS</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">The AI & Data Pipeline Behind Dance Finder</div>', unsafe_allow_html=True)

st.divider()

# ── 3 PILLARS ──
st.markdown('<div class="section-title">The 3 Pillars of This AI Prototype</div>', unsafe_allow_html=True)
st.markdown('<p style="font-family:Inter;font-size:0.8rem;color:#6a6a8a;margin-bottom:1rem;">As defined in the PDAI course framework — every AI prototype must address these three aspects.</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="pillar-card">
        <h3>🎨 Appearance & UX</h3>
        <p>Designed around the real mental model of a dancer looking for a class tonight. Ticket-style cards mimic event passes. The dark map gives immediate geographic context. Filters are fast and intuitive. The IG Story viewer builds trust by showing the raw AI source.</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="pillar-card">
        <h3>⚙️ Data & AI Pipeline</h3>
        <p>A Vision LLM (GPT-4o) reads Instagram story screenshots and studio websites daily. It extracts structured data: time, teacher, style, price, level. The pipeline runs offline so the Streamlit app stays fast at runtime. No manual data entry needed.</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="pillar-card">
        <h3>✅ Accuracy & Trust</h3>
        <p>Every class card links back to its original Instagram story screenshot — the raw source the AI read. Users can verify any extracted data themselves. The crowd predictor shows a confidence score, not a binary yes/no. Transparency is built into the design.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── PIPELINE ──
st.markdown('<div class="section-title">The Full Data Pipeline</div>', unsafe_allow_html=True)
st.markdown('<p style="font-family:Inter;font-size:0.8rem;color:#6a6a8a;margin-bottom:1.2rem;">Split into two phases: <b style="color:#c8c8e8;">Offline</b> (runs daily) and <b style="color:#c8c8e8;">Runtime</b> (the Streamlit app).</p>', unsafe_allow_html=True)

st.markdown("##### 🌙 Offline Phase — runs daily via cronjob")
p1, a1, p2, a2, p3, a3, p4 = st.columns([3,0.6,3,0.6,3,0.6,3])
with p1:
    st.markdown("""<div class="pipe-box"><div class="tag">Step 1 · Scraper</div><h4>📲 Data Collection</h4><p>Python script scrapes Barcelona dance studio websites and downloads Instagram story screenshots from teacher accounts daily.</p></div>""", unsafe_allow_html=True)
with a1:
    st.markdown('<div class="arrow">→</div>', unsafe_allow_html=True)
with p2:
    st.markdown("""<div class="pipe-box"><div class="tag">Step 2 · Vision LLM</div><h4>🤖 AI Extraction</h4><p>GPT-4o reads each image. Prompt: <em>"Extract time, teacher, style, price, level."</em> Returns structured JSON automatically.</p></div>""", unsafe_allow_html=True)
with a2:
    st.markdown('<div class="arrow">→</div>', unsafe_allow_html=True)
with p3:
    st.markdown("""<div class="pipe-box"><div class="tag">Step 3 · Storage</div><h4>🗄️ Clean Database</h4><p>Saved as <code>classes.json</code> for today's view and appended to <code>classes_history.csv</code> for the crowd prediction model.</p></div>""", unsafe_allow_html=True)
with a3:
    st.markdown('<div class="arrow">→</div>', unsafe_allow_html=True)
with p4:
    st.markdown("""<div class="pipe-box"><div class="tag">Step 4 · ML Model</div><h4>📊 Crowd Predictor</h4><p>Random Forest trained on historical attendance data predicts how full each class will be. Saved as <code>model.pkl</code>, loaded at runtime.</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("##### ☀️ Runtime Phase — the Streamlit app")
r1, ra, r2 = st.columns([3,0.6,3])
with r1:
    st.markdown("""<div class="pipe-box" style="border-left-color:rgba(79,142,247,0.6);"><div class="tag" style="background:rgba(79,142,247,0.1);color:#90b8ff;border-color:rgba(79,142,247,0.25);">Runtime · Load</div><h4>📂 Load Clean Data</h4><p>Reads <code>classes.json</code> and <code>model.pkl</code> at startup. No scraping, no API calls — instant load time.</p></div>""", unsafe_allow_html=True)
with ra:
    st.markdown('<div class="arrow">→</div>', unsafe_allow_html=True)
with r2:
    st.markdown("""<div class="pipe-box" style="border-left-color:rgba(79,142,247,0.6);"><div class="tag" style="background:rgba(79,142,247,0.1);color:#90b8ff;border-color:rgba(79,142,247,0.25);">Runtime · Display</div><h4>🎫 Present to User</h4><p>Ticket cards, interactive map, teacher profiles, crowd badges and IG story previews rendered dynamically based on filters.</p></div>""", unsafe_allow_html=True)

st.divider()

# ── AI MODELS ──
st.markdown('<div class="section-title">The Two AI Models</div>', unsafe_allow_html=True)
b1, b2 = st.columns(2)
with b1:
    st.markdown("""<div class="pipe-box"><div class="tag">Model 1 · Crowd Predictor</div><h4>⚡ Will This Class Fill Up?</h4><p>Every day the scraper logs: date, weekday, teacher, style, studio, weather, spots_filled. A Random Forest or XGBoost model trains on this history to predict crowd levels. The <code>crowd_score</code> in the app is this model's output.</p></div>""", unsafe_allow_html=True)
with b2:
    st.markdown("""<div class="pipe-box"><div class="tag">Model 2 · Recommender</div><h4>💡 What Should I Try Next?</h4><p>As users interact (saving classes, booking, rating), a collaborative filtering model builds a preference profile. It recommends classes based on similarity to other dancers — like Spotify's Discover Weekly, but for dance classes.</p></div>""", unsafe_allow_html=True)

st.divider()

# ── TECH STACK ──
st.markdown('<div class="section-title">Tech Stack</div>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("""<div class="tech-col"><h4>Frontend</h4><ul><li>Streamlit</li><li>Folium (interactive map)</li><li>Custom HTML/CSS ticket cards</li><li>streamlit-folium</li></ul></div>""", unsafe_allow_html=True)
with t2:
    st.markdown("""<div class="tech-col"><h4>AI & Data Pipeline</h4><ul><li>GPT-4o Vision API</li><li>BeautifulSoup (scraper)</li><li>instaloader (Instagram)</li><li>scikit-learn / XGBoost</li></ul></div>""", unsafe_allow_html=True)
with t3:
    st.markdown("""<div class="tech-col"><h4>Infrastructure</h4><ul><li>JSON / CSV storage</li><li>AWS EC2 deployment</li><li>GitHub version control</li><li>Cronjob daily pipeline</li></ul></div>""", unsafe_allow_html=True)

st.markdown('<br><p style="font-family:Inter;font-size:0.7rem;color:#3a3a5a;text-align:center;">Dance Finder · PDAI Assignment 1 · Prototype uses mock data to simulate the full AI pipeline</p>', unsafe_allow_html=True)
