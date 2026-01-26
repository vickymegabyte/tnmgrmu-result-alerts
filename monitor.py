import requests
import hashlib
import os

URL = "https://cms2results.tnmgrmuexam.ac.in/#/ExamResult"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Only B.PHARM keywords
KEYWORDS = [
    "B.PHARM",
    "B PHARM",
    "BPHARM",
    "B.PHARM.",
    "B.PHARM. ",
    "BACHELOR OF PHARMACY"
]

def get_page_content():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()
    return r.text.upper()

def send_telegram():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": "🎓 B.PHARM RESULT PUBLISHED (TNMGRMU)\n\nCheck now:\nhttps://cms2results.tnmgrmuexam.ac.in/#/ExamResult"
    })

def main():
    content = get_page_content()
    new_hash = hashlib.md5(content.encode()).hexdigest()

    try:
        with open("hash.txt", "r") as f:
            old_hash = f.read()
    except FileNotFoundError:
        old_hash = ""

    # Save new hash
    with open("hash.txt", "w") as f:
        f.write(new_hash)

    # Alert only if page changed AND B.PHARM exists
    if new_hash != old_hash and any(k in content for k in KEYWORDS):
        send_telegram()

if __name__ == "__main__":
    main()
