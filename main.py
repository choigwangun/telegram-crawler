import os
import time
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

last_seen_title = ""
TARGET_URL = "https://sexbam32.top/a18"

def check_new_post():
    global last_seen_title
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(TARGET_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        post = soup.find('article')

        if not post:
            print("게시글 없음")
            return

        title = post.get_text(strip=True)
        link_tag = post.find('a')
        link = link_tag['href'] if link_tag else TARGET_URL

        if title != last_seen_title:
            print(f"새 게시글: {title}")
            last_seen_title = title
            send_telegram(f"📢 새 게시글: {title}\n🔗 {link}")
        else:
            print("변경 없음")

    except Exception as e:
        print(f"오류: {e}")

while True:
    check_new_post()
    time.sleep(600)
