import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Try Anthropic first, fallback to Gemini
USE_GEMINI = False
client = None

try:
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        client = anthropic.Anthropic(api_key=api_key)
        USE_GEMINI = False
except:
    pass

if client is None:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    USE_GEMINI = True

def load_classes() -> list:
    try:
        with open("classes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def classes_to_context(classes: list) -> str:
    if not classes:
        return "No classes available right now."
    lines = []
    for i, c in enumerate(classes):
        lines.append(
            f"Class {i+1}: {c.get('style','')} | {c.get('level','')} | "
            f"{c.get('studio','')} | {c.get('address','')} | "
            f"Teacher: {c.get('teacher',{}).get('name','')} | "
            f"Time: {c.get('time_start','')}–{c.get('time_end','')} | "
            f"Price: {c.get('price_label','')} | "
            f"Free: {c.get('free_trial',False)} | "
            f"Crowd: {int(c.get('crowd_score',0.5)*100)}% | "
            f"Instagram: {c.get('instagram_studio','')} | "
            f"Maps: {c.get('maps_link','')} | "
            f"Website: {c.get('website','')}"
        )
    return "\n".join(lines)

def get_filter_instructions(user_query: str, classes: list) -> dict:
    all_styles = list(set(c.get("style","") for c in classes))
    all_levels = ["Beginner","Intermediate","Advanced","All Levels"]
    filter_prompt = f"""
You are a filter extractor for a dance class finder app.
Given a user search query, extract filter parameters and return ONLY valid JSON, no markdown.

Available styles: {json.dumps(all_styles)}
Available levels: {json.dumps(all_levels)}

Return JSON with keys:
- "styles": array of matching styles (empty = all)
- "levels": array of matching levels (empty = all)
- "free_only": true if user wants free classes
- "keywords": array of keywords

User query: "{user_query}"
Return ONLY the JSON object.
"""
    try:
        if USE_GEMINI:
            response = gemini_model.generate_content(filter_prompt)
            raw = response.text.strip()
        else:
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=300,
                messages=[{"role":"user","content":filter_prompt}]
            )
            raw = response.content[0].text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"Filter extraction failed: {e}")
        return {"styles":[],"levels":[],"free_only":False,"keywords":[]}

def chat(user_message: str, conversation_history: list, classes: list) -> tuple[str, list]:
    context = classes_to_context(classes)
    system_prompt = f"""You are Dance Finder AI, a friendly assistant for finding dance classes in Barcelona.
Use the class data below to answer questions. Always mention studio, teacher, time, price and links.
Answer in the same language the user writes in (English, German, Spanish, Catalan).
Keep responses under 200 words.

Today's classes:
{context}
"""
    conversation_history.append({"role":"user","content":user_message})

    try:
        if USE_GEMINI:
            full_prompt = system_prompt + "\n\nConversation:\n"
            for turn in conversation_history:
                full_prompt += f"{turn['role'].upper()}: {turn['content']}\n"
            full_prompt += "ASSISTANT:"
            response = gemini_model.generate_content(full_prompt)
            assistant_message = response.text
        else:
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=500,
                system=system_prompt,
                messages=conversation_history
            )
            assistant_message = response.content[0].text

        conversation_history.append({"role":"assistant","content":assistant_message})
        return assistant_message, conversation_history

    except Exception as e:
        error_msg = f"Sorry, I couldn't process that. Please try again! ({str(e)})"
        conversation_history.append({"role":"assistant","content":error_msg})
        return error_msg, conversation_history

def reset_conversation() -> list:
    return []
