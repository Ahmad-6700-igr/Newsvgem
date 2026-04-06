import feedparser
import requests
import re
import json
import os # Tambahkan modul os

# ================= KONEKSI & KONFIGURASI =================
# Mengambil dari Environment Variables (GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validasi keamanan: Hentikan script jika kredensial kosong
if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY]):
    print("[-] FATAL ERROR: Kredensial tidak ditemukan di Environment Variables!")
    exit(1)

# RSS Feed Google News
RSS_URL = "https://news.google.com/rss/search?q=AI+OR+coding+OR+developer+OR+Android+when:1d&hl=en-US&gl=US&ceid=US:en"

# ... (Sisa kode fetch_and_score_news, process_with_ai, dan send_to_telegram SAMA PERSIS seperti sebelumnya) ...
