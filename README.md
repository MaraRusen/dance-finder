# 🕺 DanceFinder BCN
**Discover dance classes in Barcelona — powered by AI**

> PDAI Assignment 2 · Mara Rüsen · ESADE Business School · 2026

🌐 **[Live App](https://dance-finder-ax2tbcexhyhjqsjij2exkw.streamlit.app)** | 💻 **[GitHub](https://github.com/MaraRusen/dance-finder)**

---

## What is Dance Finder BCN?

Finding a dance class in Barcelona means scrolling through dozens of Instagram accounts and studio websites with no central platform. Dance Finder BCN solves this with an AI-powered discovery platform — showing who is teaching, where, when, at what price, and how full the class is.

---

## The 3 LLMs

| LLM | Role |
|---|---|
| **Gemini 1.5 Flash** | Scrapes real studio websites → extracts structured JSON |
| **Gemini / Claude AI** | Natural language search + multi-turn RAG chatbot |
| **Cohere Rerank** | Semantically re-sorts results by query relevance |

---

## Features

- 🤖 Natural language AI search — powered by Claude/Gemini
- 🌐 Real studio data — 17 Barcelona studios with verified links
- 📍 Interactive Folium map with crowd-level markers
- ⭐ Community ratings stored in SQLite
- 📩 Email notifications via Gmail SMTP
- 🎂 Age group filter (Kids / Teens / Adults)
- 🎵 20+ dance styles

---

## Project Structure
```
dance-finder/
├── app.py           # Main Streamlit app
├── chatbot.py       # Gemini/Claude chatbot + filter extraction
├── scraper.py       # Gemini web scraper parser
├── reranker.py      # Cohere semantic reranking
├── database.py      # SQLite ratings + email notifications
├── classes.json     # Curated class data (16 real Barcelona classes)
├── studios.json     # 17 real Barcelona studios
├── requirements.txt
└── pages/
    └── about.py     # Pipeline explanation page
```

---

## How to Run Locally
```bash
git clone https://github.com/MaraRusen/dance-finder.git
cd dance-finder
micromamba activate jose
pip install -r requirements.txt
streamlit run app.py
```

Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
COHERE_API_KEY=your_key
GMAIL_USER=your_email
GMAIL_APP_PASSWORD=your_app_password
```

---

## Tech Stack

| Category | Tool |
|---|---|
| Frontend | Streamlit + Custom CSS |
| Map | Folium + streamlit-folium |
| LLM 1 | Gemini 1.5 Flash |
| LLM 2 | Claude / Gemini AI |
| LLM 3 | Cohere Rerank |
| Scraping | BeautifulSoup + requests |
| Database | SQLite |
| Deployment | Streamlit Cloud |

---

*Built for PDAI · ESADE Business School · Barcelona · 2026*
