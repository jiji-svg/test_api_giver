import requests
import os
import datetime
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

API_KEY = os.getenv('API_KEY')
SLACK_WEBHOOK_URL = os.getenv('CAT_SLACK_WEBHOOK_URL')

# 추후에 API KEY 필요하면 쓸것
# cat_url = f'https://api.thecatapi.com/v1/images/search?limit=10&api_key={API_KEY}'

cat_url = f'https://api.thecatapi.com/v1/images/search?limit=10'

def get_cat_image():
    response = requests.get(cat_url)
    if response.status_code == 200:
        data = response.json()
        return [item['url'] for item in data]
    else:
        print(f"API 호출 실패: {response.status_code}, {response.text}")
        return []

def send_slack_message(image_urls):
    now = datetime.datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

    # 헤더 메시지
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{now} 기준 랜덤 고양이 사진 10장입니다 😺*"
            }
        }
    ]

    # 각 이미지 블록 추가
    for url in image_urls:
        blocks.append({
            "type": "image",
            "image_url": url,
            "alt_text": "고양이 사진"
        })

    slack_data = {"blocks": blocks}

    response = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    if response.status_code != 200:
        print(f"Slack 전송 실패: {response.status_code}, {response.text}")

if __name__ == "__main__":
    cat_image = get_cat_image()
    send_slack_message(cat_image)