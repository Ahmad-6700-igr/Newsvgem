import os
import time
import feedparser
import requests
import re
from bs4 import BeautifulSoup
from google import genai

# ===== ENV =====
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# ===== RSS =====
RSS_FEEDS = [
    "https://hnrss.org/frontpage?points=100",
    "https://android-developers.googleblog.com/atom.xml",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]

KEYWORDS = {
    "ai": 5,
    "android": 5,
    "developer": 3,
    "coding": 3,
    "python": 3,
    "kotlin": 3,
    "llm": 5,
    "gpt": 5
}

# ===== CLEAN =====
def clean_html(text):
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

# ===== SCORING =====
def score(text):
    s = 0
    for k, v in KEYWORDS.items():
        if k in text.lower():
            s += v
    return s

# ===== GET NEWS =====
def get_best_news():
    articles = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = clean_html(entry.title)
                summary = clean_html(entry.get("summary", ""))
                s = score(title + summary)
                articles.append((s, title, entry.link))
        except:
            continue

    if not articles:
        return (0, "No news found", "")

    return sorted(articles, reverse=True)[0]

# ===== AI FUNCTIONS (FIXED GENAI) =====
def ai_generate(prompt):
    try:
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return res.text
    except Exception as e:
        return f"AI Error: {e}"

def ai_translate(text):
    return ai_generate(f"Translate to Indonesian:\n{text}")

def ai_summary(text):
    return ai_generate(f"Summarize into 5 bullet points:\n{text}")

def ai_opinion(text):
    return ai_generate(f"Give expert opinion about this tech news:\n{text}")

# ===== SEND TELEGRAM =====
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        })
    except Exception as e:
        print("Telegram Error:", e)

# ===== MAIN LOOP =====
def run_session():
    start = time.time()

    while time.time() - start < 3600:  # 1 jam
        try:
            s, title, link = get_best_news()

            translate = ai_translate(title)
            summary = ai_summary(title)
            opinion = ai_opinion(title)

            message = f"""
🔥 NEWS TERPILIH

📰 {title}

🌐 {link}

🇮🇩 Translate:
{translate}

📌 Summary:
{summary}

🧠 Opini:
{opinion}
"""

            send_message(message)

            time.sleep(900)  # tiap 15 menit

        except Exception as e:
            print("Loop Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    run_session()