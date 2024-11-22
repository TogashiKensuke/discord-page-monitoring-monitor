import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import difflib
import json

# 設定
TARGET_URL = "監視したいページのURL"
DISCORD_WEBHOOK_URL = "通知したいDiscordのWebhook URL"
CHECK_INTERVAL = 300  # チェック間隔（秒）

# ブラウザのように振る舞うためのヘッダー
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def send_discord_notification(message):
    payload = {
        "content": message
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def get_page_content(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    # スクリプトとスタイルを除去
    for script in soup(["script", "style"]):
        script.decompose()
    return soup.get_text()

def monitor_website():
    print(f"監視開始: {TARGET_URL}")
    previous_content = get_page_content(TARGET_URL)

    send_discord_notification('監視を開始しました！')
    
    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            current_content = get_page_content(TARGET_URL)
            
            if current_content != previous_content:
                message = f"ページが更新されました！\n時刻: {datetime.now()}\nURL: {TARGET_URL}"
                send_discord_notification(message)
                print(f"更新を検知: {datetime.now()}")
                previous_content = current_content
            else:
                print(f"変更なし: {datetime.now()}")
                
        except Exception as e:
            error_message = f"エラーが発生しました: {str(e)}"
            print(error_message)
            send_discord_notification(error_message)

if __name__ == "__main__":
    monitor_website()