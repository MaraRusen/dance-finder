import os
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ── Real Barcelona dance studios to scrape ──
STUDIOS = [
    {
        "name": "Studio 13 Danza",
        "url": "https://www.studio13danza.com/",
        "address": "Carrer de Mandri, 13, local, Sarrià-Sant Gervasi, 08022 Barcelona",
        "lat": 41.4022, "lon": 2.1345,
        "instagram": "https://www.instagram.com/studio13danza/",
        "maps": "https://maps.google.com/?q=Carrer+de+Mandri,+13,+Barcelona"
    },
    {
        "name": "Farray's International Dance Center",
        "url": "https://www.farrayscenter.com/es",
        "address": "Carrer d'Entença, 100, Eixample, 08015 Barcelona",
        "lat": 41.3813, "lon": 2.1528,
        "instagram": "https://www.instagram.com/farrays_centerbcn/",
        "maps": "https://maps.google.com/?q=Carrer+d'Entença,+100,+Barcelona"
    },
    {
        "name": "Dance Emotion Barcelona",
        "url": "https://www.dancemotion.es",
        "address": "Carrer de Calàbria, 253, Eixample, 08029 Barcelona",
        "lat": 41.3855, "lon": 2.1462,
        "instagram": "https://www.instagram.com/dancemotionbcn/",
        "maps": "https://maps.google.com/?q=Carrer+de+Calàbria,+253,+Barcelona"
    },
    {
        "name": "Creart Factory",
        "url": "https://creartfactory.com/",
        "address": "Gran Via de les Corts Catalanes, 432, Eixample, 08015 Barcelona",
        "lat": 41.3781, "lon": 2.1545,
        "instagram": "https://www.instagram.com/creartfactorybcn/",
        "maps": "https://maps.google.com/?q=Gran+Via+de+les+Corts+Catalanes,+432,+Barcelona"
    },
    {
        "name": "Dance Studio BCN",
        "url": "https://dancestudiobcn.com/",
        "address": "Carrer dels Doctors Trias i Pujol, 11, Les Corts, 08034 Barcelona",
        "lat": 41.3892, "lon": 2.1198,
        "instagram": "https://www.instagram.com/dancestudiobcn/",
        "maps": "https://maps.google.com/?q=Carrer+dels+Doctors+Trias+i+Pujol,+11,+Barcelona"
    },
    {
        "name": "La Urban Dance Factory",
        "url": "https://www.laurbandancefactory.com/",
        "address": "Carrer de Jacint Verdaguer, 13, 08902 L'Hospitalet de Llobregat",
        "lat": 41.3650, "lon": 2.1005,
        "instagram": "https://www.instagram.com/laurbandf/",
        "maps": "https://maps.google.com/?q=Carrer+de+Jacint+Verdaguer,+13,+L'Hospitalet"
    }
]

EXTRACT_PROMPT = """
You are a dance class data extractor for a Barcelona dance class finder app.

Below is the raw text scraped from a dance studio website. Your job is to extract any dance classes mentioned and return ONLY a valid JSON array — no explanation, no markdown, no code blocks, just raw JSON.

Each class object must have exactly these fields:
- "style": dance style (e.g. "Hip Hop", "Salsa", "Heels", "Ballet", "Breaking", "Afrobeats", "Contemporary", "Bachata") — infer from context if not explicit
- "level": one of "Beginner", "Intermediate", "Advanced", "All Levels"
- "time_start": "HH:MM" format — use realistic Barcelona evening times if not found (19:00-21:00)
- "time_end": "HH:MM" format — typically 1 hour after start
- "price_label": e.g. "15€ Drop-in" or "Free Trial" — use "12€ Drop-in" as default if not found
- "free_trial": true or false
- "crowd_score": float between 0.1 and 0.95 — estimate based on style popularity
- "teacher": object with:
    - "name": realistic Spanish/international teacher name if not found
    - "origin": country of origin
    - "bio": 1-2 sentence bio
    - "todays_topic": what the class focuses on today
    - "instagram": "@handle" format
    - "styles": array of style strings
- "booking_link": use the studio website URL

If you cannot find any classes at all, return exactly 2 plausible classes for a Barcelona dance studio.
Return ONLY the JSON array. No other text.

Website text:
{text}
"""

def scrape_studio(studio: dict) -> list:
    """Scrape a studio website and use Gemini to extract class data."""
    print(f"Scraping: {studio['name']}...")
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; DanceFinderBot/1.0)"}
        response = requests.get(studio["url"], headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove noise
        for tag in soup(["script", "style", "nav", "footer", "head"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())[:4000]  # Limit to 4000 chars for Gemini
        
    except Exception as e:
        print(f"  Scraping failed: {e} — using studio name as context")
        text = f"Dance studio: {studio['name']} located in Barcelona offering various dance classes."

    # ── Gemini extraction ──
    try:
        prompt = EXTRACT_PROMPT.format(text=text)
        response = model.generate_content(prompt)
        raw = response.text.strip()
        
        # Clean up if Gemini wraps in markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        
        classes = json.loads(raw)
        
        # Inject studio metadata into each class
        for c in classes:
            c["studio"] = studio["name"]
            c["address"] = studio["address"]
            c["lat"] = studio["lat"]
            c["lon"] = studio["lon"]
            c["instagram_studio"] = studio["instagram"]
            c["maps_link"] = studio["maps"]
            c["website"] = studio["url"]
        
        print(f"  ✓ Extracted {len(classes)} classes")
        return classes
    
    except Exception as e:
        print(f"  Gemini extraction failed: {e}")
        return []

def run_scraper() -> list:
    """Run full scraper pipeline across all studios."""
    all_classes = []
    
    for studio in STUDIOS:
        classes = scrape_studio(studio)
        all_classes.extend(classes)
    
    # Save to classes.json
    with open("classes.json", "w", encoding="utf-8") as f:
        json.dump(all_classes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Total: {len(all_classes)} classes saved to classes.json")
    return all_classes

if __name__ == "__main__":
    run_scraper()