# 🕺 Dance Finder
**Discover dance classes in Barcelona — powered by AI**

> PDAI Assignment 1 · Mara Rüsen · ESADE Business School · 2026

---

## What is Dance Finder?

Finding a dance class in Barcelona today means scrolling through dozens of Instagram stories, checking multiple studio websites, and still not knowing if the class is full or who the teacher is.

**Dance Finder solves this.** It aggregates all dance classes in Barcelona into one beautiful interface — showing you who is teaching, where, when, at what price, and how full the class is expected to be. All in real time.

---

## Live Demo

🌐 **[dance-finder.streamlit.app](https://dance-finder.streamlit.app)** ← coming soon

---

## The 3 Pillars of the Prototype

This prototype was built around the three core aspects of AI product development as defined in the PDAI course:

### 1. 🎨 Appearance & User Experience
- Dark, editorial design inspired by real Barcelona dance studios
- **Custom HTML/CSS Ticket Cards** — classes displayed as event passes, not boring tables
- Interactive **Folium map** with color-coded pins (availability level)
- Sidebar-free layout — all filters on one clean bar at the top
- Hero section with background video

### 2. ⚙️ Data & AI Pipeline
The pipeline is intentionally separated into **offline** (data collection) and **runtime** (the app):

```
OFFLINE — runs daily via cronjob
────────────────────────────────────────────────────
[Instagram Stories + Studio Websites]
        ↓  scraper.py (BeautifulSoup + instaloader)
[Raw screenshots + unstructured text]
        ↓  extractor.py (GPT-4o Vision API)
[Structured JSON: time, teacher, price, style, level]
        ↓
[classes.json]  ←── what the app loads
[classes_history.csv]  ←── grows daily → trains ML model

RUNTIME — the Streamlit app
────────────────────────────────────────────────────
[classes.json] → map, ticket cards, filters
[model.pkl]    → crowd_score prediction per class
```

> In this prototype, `classes.json` is a mock dataset that simulates the output of the full AI pipeline.

### 3. ✅ Accuracy & Transparency
- Every class card has a **"View Original IG Story"** button — showing the raw screenshot the AI extracted data from
- The **crowd score** is shown as a percentage, not a binary label — the user interprets the prediction themselves
- Transparency is a core design principle: users can always verify what the AI extracted

---

## AI Models

### 🔥 Crowd Predictor
Over weeks of data collection, `classes_history.csv` accumulates rows of: `date, weekday, teacher, style, studio, weather, spots_filled`. A **Random Forest** model trains on this history and predicts how full each class will be. The `crowd_score` field in the JSON is this model's output.

### 💡 Recommender (planned)
As users interact with the app (saving classes, booking, rating), a **collaborative filtering** model builds a preference profile — recommending classes similar to what the user has enjoyed before. Think Spotify's Discover Weekly, but for dance classes in Barcelona.

---

## App Features

| Feature | Description | Streamlit Widget |
|---|---|---|
| 🗺️ Interactive Map | Color-coded studio pins, clickable popups | `streamlit-folium` |
| 🎫 Ticket Cards | Custom HTML/CSS event-style class cards | `st.markdown` (HTML) |
| 📅 Date Picker | Browse classes by date | `st.date_input` |
| 🎵 Style Filter | Filter by dance style | `st.multiselect` |
| 👤 Teacher Filter | Filter by specific teacher | `st.multiselect` |
| 🎯 Level Filter | Beginner / Intermediate / Advanced | `st.multiselect` |
| 🎁 Free Toggle | Show only free trial classes | `st.toggle` |
| 📊 Metrics Row | Classes today, free trials, selling fast | `st.metric` |
| ℹ️ Teacher Bio | Expandable teacher profile + today's topic | `st.expander` |
| 📸 IG Story Viewer | Original AI source screenshot | `st.expander` |

> All widgets marked with ✳️ were **not covered in class** — added to meet the assignment's advanced widget requirement.

---

## Project Structure

```
dance-finder/
│
├── app.py                  # Main Streamlit app (Dance Finder)
├── classes.json            # Mock dataset — simulates AI pipeline output
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes video + cache files
│
├── pages/
│   └── about.py            # "How It Works" page — full pipeline explanation
│
└── static/
    └── dance.mov           # Hero background video (excluded from git)
```

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/MaraRusen/dance-finder.git
cd dance-finder

# 2. Activate your environment
micromamba activate Jose   # or your preferred environment

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## Dependencies

```
streamlit>=1.32.0
folium>=0.16.0
streamlit-folium>=0.20.0
```

---

## Tech Stack

| Category | Tools |
|---|---|
| **Frontend** | Streamlit, Folium, Custom HTML/CSS |
| **AI Extraction** | GPT-4o Vision API (simulated in prototype) |
| **Web Scraping** | BeautifulSoup, instaloader |
| **ML Model** | scikit-learn / XGBoost (simulated via mock crowd_score) |
| **Storage** | JSON (today's classes), CSV (historical data) |
| **Deployment** | Streamlit Cloud / AWS EC2 |
| **Version Control** | GitHub |

---

## Pages

| Page | File | Description |
|---|---|---|
| 🕺 Dance Finder | `app.py` | Main app — map, filters, ticket cards |
| ⚙️ How It Works | `pages/about.py` | Full AI pipeline explanation, tech stack, model details |

---

*Built for the Prototyping Products with Data & AI (PDAI) course · ESADE Business School · Barcelona · 2026*