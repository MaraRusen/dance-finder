import sqlite3
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "dance_finder.db"

# ── INIT DATABASE ──
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            signup_date TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studio_name TEXT NOT NULL,
            class_style TEXT,
            stars INTEGER NOT NULL CHECK(stars >= 1 AND stars <= 5),
            user_email TEXT,
            comment TEXT,
            date TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            studio_name TEXT NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()

# ── USERS ──
def add_user(email: str) -> dict:
    """Register a new user email. Returns status."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (email, signup_date) VALUES (?, ?)",
            (email.lower().strip(), datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": f"Welcome! {email} registered successfully."}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "message": "Email already registered!"}

def user_exists(email: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email.lower().strip(),))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_all_users() -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT email FROM users")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# ── RATINGS ──
def add_rating(studio_name: str, stars: int, user_email: str = None,
               class_style: str = None, comment: str = None) -> dict:
    """Add a star rating for a studio."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO ratings (studio_name, class_style, stars, user_email, comment, date)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (studio_name, class_style, stars, user_email, comment, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Rating saved!"}

def get_studio_rating(studio_name: str) -> dict:
    """Get average rating and count for a studio."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT AVG(stars), COUNT(*) FROM ratings WHERE studio_name = ?",
        (studio_name,)
    )
    row = c.fetchone()
    conn.close()
    avg = round(row[0], 1) if row[0] else None
    count = row[1]
    return {"average": avg, "count": count}

def get_all_ratings() -> list:
    """Get all ratings for display."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT studio_name, class_style, stars, user_email, comment, date
        FROM ratings ORDER BY date DESC LIMIT 50
    """)
    rows = c.fetchall()
    conn.close()
    return [
        {
            "studio": r[0], "style": r[1], "stars": r[2],
            "email": r[3], "comment": r[4], "date": r[5]
        }
        for r in rows
    ]

# ── NOTIFICATIONS ──
def subscribe_to_studio(email: str, studio_name: str) -> dict:
    """Subscribe user to notifications for a studio."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Check if already subscribed
    c.execute(
        "SELECT id FROM notifications WHERE user_email = ? AND studio_name = ?",
        (email.lower().strip(), studio_name)
    )
    if c.fetchone():
        conn.close()
        return {"success": False, "message": "Already subscribed!"}
    c.execute(
        "INSERT INTO notifications (user_email, studio_name) VALUES (?, ?)",
        (email.lower().strip(), studio_name)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Subscribed to {studio_name}!"}

def get_subscribers_for_studio(studio_name: str) -> list:
    """Get all emails subscribed to a studio."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT user_email FROM notifications WHERE studio_name = ? AND active = 1",
        (studio_name,)
    )
    emails = [row[0] for row in c.fetchall()]
    conn.close()
    return emails

def get_user_subscriptions(email: str) -> list:
    """Get all studios a user is subscribed to."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT studio_name FROM notifications WHERE user_email = ? AND active = 1",
        (email.lower().strip(),)
    )
    studios = [row[0] for row in c.fetchall()]
    conn.close()
    return studios

# ── EMAIL NOTIFICATIONS ──
def send_notification_email(to_email: str, subject: str, body: str) -> bool:
    """Send email via Gmail SMTP."""
    gmail_user = os.getenv("GMAIL_USER", "mararsn1001@gmail.com")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_password:
        print("No Gmail App Password set — skipping email")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Dance Finder BCN <{gmail_user}>"
        msg["To"] = to_email

        html_body = f"""
        <html>
        <body style="background:#060612;color:#c8c8e8;font-family:Inter,sans-serif;padding:30px;">
            <h1 style="font-family:Georgia,serif;color:#7c5cbf;font-size:2rem;">🕺 Dance Finder BCN</h1>
            <div style="background:#0c0c22;border:1px solid rgba(124,92,191,0.3);
                        border-radius:12px;padding:20px;margin-top:16px;">
                {body}
            </div>
            <p style="color:#6a6a8a;font-size:0.75rem;margin-top:20px;">
                You're receiving this because you subscribed on Dance Finder BCN.<br>
                Barcelona's real-time dance class discovery platform.
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, msg.as_string())

        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

def notify_new_class(studio_name: str, class_info: dict):
    """Notify all subscribers of a studio about a new class."""
    subscribers = get_subscribers_for_studio(studio_name)
    if not subscribers:
        return

    subject = f"🕺 New class at {studio_name}!"
    body = f"""
    <h2 style="color:#eeeeff;">New class just added!</h2>
    <p><b style="color:#90b8ff;">{class_info.get('style', '')}</b> · {class_info.get('level', '')}</p>
    <p>📍 <b>{studio_name}</b></p>
    <p>⏰ {class_info.get('time_start', '')} – {class_info.get('time_end', '')}</p>
    <p>👤 {class_info.get('teacher', {}).get('name', '')}</p>
    <p>💶 {class_info.get('price_label', '')}</p>
    <a href="https://dance-finder-ax2tbcexhyhjqsjij2exkw.streamlit.app"
       style="display:inline-block;margin-top:16px;padding:10px 20px;
              background:#7c5cbf;color:#fff;border-radius:6px;text-decoration:none;">
        View on Dance Finder →
    </a>
    """

    for email in subscribers:
        send_notification_email(email, subject, body)

# ── CROWD SCORE HEURISTIC ──
def estimate_crowd_score(style: str, time_start: str, weekday: int = None) -> float:
    """
    Rule-based crowd score estimation.
    weekday: 0=Monday, 6=Sunday
    Returns float 0.0–1.0
    """
    if weekday is None:
        weekday = datetime.now().weekday()

    try:
        hour = int(time_start.split(":")[0])
    except:
        hour = 19

    # Base score by style popularity
    style_base = {
        "Salsa": 0.75, "Bachata": 0.72, "Hip Hop": 0.70,
        "Reggaeton": 0.68, "Heels": 0.65, "Latin": 0.70,
        "Afrobeats": 0.60, "Dancehall": 0.58, "Contemporary": 0.50,
        "Ballet": 0.45, "Breaking": 0.55, "Jazz": 0.48,
        "Flamenco": 0.52, "House": 0.50, "Krump": 0.40,
        "Waacking": 0.45, "Voguing": 0.42, "Tap": 0.38,
        "Commercial": 0.60, "Popping": 0.50, "Locking": 0.48
    }
    base = style_base.get(style, 0.55)

    # Weekday multiplier
    weekday_mult = {0: 0.7, 1: 0.75, 2: 0.8, 3: 0.85, 4: 0.95, 5: 1.0, 6: 0.9}
    mult = weekday_mult.get(weekday, 0.8)

    # Prime time bonus (18:00–21:00)
    if 18 <= hour <= 21:
        time_bonus = 0.15
    elif 10 <= hour <= 14:
        time_bonus = 0.05
    else:
        time_bonus = -0.05

    score = min(0.97, max(0.15, base * mult + time_bonus))
    return round(score, 2)

# Initialize DB on import
init_db()