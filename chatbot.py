import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_classes() -> list:
    """Load current classes from classes.json"""
    try:
        with open("classes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def classes_to_context(classes: list) -> str:
    """Convert classes list to readable context string for Claude."""
    if not classes:
        return "No classes available right now."
    
    lines = []
    for i, c in enumerate(classes):
        lines.append(f"""
Class {i+1}:
- Style: {c.get('style', 'Unknown')}
- Level: {c.get('level', 'All Levels')}
- Studio: {c.get('studio', 'Unknown')}
- Address: {c.get('address', 'Barcelona')}
- Teacher: {c.get('teacher', {}).get('name', 'Unknown')}
- Time: {c.get('time_start', '?')} - {c.get('time_end', '?')}
- Price: {c.get('price_label', 'Unknown')}
- Free Trial: {c.get('free_trial', False)}
- Crowd: {int(c.get('crowd_score', 0.5) * 100)}% full
- Instagram: {c.get('instagram_studio', '')}
- Maps: {c.get('maps_link', '')}
- Website: {c.get('website', '')}
""")
    return "\n".join(lines)

def get_filter_instructions(user_query: str, classes: list) -> dict:
    """
    Ask Claude to extract filter parameters from natural language query.
    Returns a dict with filter keys that the Streamlit app can apply directly.
    This is the non-straightforward part: LLM output is post-processed
    by Python to control the UI state.
    """
    all_styles = list(set(c.get("style", "") for c in classes))
    all_levels = ["Beginner", "Intermediate", "Advanced", "All Levels"]
    
    filter_prompt = f"""
You are a filter extractor for a dance class finder app.

Given a user search query, extract the filter parameters and return ONLY valid JSON.
No explanation, no markdown, just raw JSON.

Available styles: {json.dumps(all_styles)}
Available levels: {json.dumps(all_levels)}

Return a JSON object with these keys:
- "styles": array of matching styles from available styles (empty array = all)
- "levels": array of matching levels (empty array = all)
- "free_only": true if user wants free classes, false otherwise
- "keywords": array of important keywords from the query for further matching

User query: "{user_query}"

Return ONLY the JSON object.
"""
    
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": filter_prompt}]
        )
        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"Filter extraction failed: {e}")
        return {"styles": [], "levels": [], "free_only": False, "keywords": []}

def chat(user_message: str, conversation_history: list, classes: list) -> tuple[str, list]:
    """
    Multi-turn Claude chatbot with dance class data as RAG context.
    Returns (assistant_response, updated_history)
    """
    context = classes_to_context(classes)
    
    system_prompt = f"""You are Dance Finder AI, a friendly and knowledgeable assistant for finding dance classes in Barcelona.

You have access to today's real dance class data. Use it to answer questions accurately.
When recommending classes, always mention the studio name, teacher, time, price, and provide the maps/instagram links if available.
Be warm, enthusiastic about dance, and concise. Answer in the same language the user writes in (English, German, Spanish, Catalan).

Today's available classes in Barcelona:
{context}

Important rules:
- Only recommend classes from the data above
- Always include practical info: time, price, location
- If asked about a style not available today, say so honestly
- Keep responses under 200 words
- Use emojis sparingly but naturally
"""

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=system_prompt,
            messages=conversation_history
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant", 
            "content": assistant_message
        })
        
        return assistant_message, conversation_history
    
    except Exception as e:
        error_msg = f"Sorry, I couldn't process that. Please try again! ({str(e)})"
        conversation_history.append({
            "role": "assistant",
            "content": error_msg
        })
        return error_msg, conversation_history

def reset_conversation() -> list:
    """Reset conversation history."""
    return []