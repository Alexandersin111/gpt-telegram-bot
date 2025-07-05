from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    if 'message' not in data:
        return 'ok'

    chat_id = data['message']['chat']['id']
    user_message = data['message'].get('text', '')

    if not user_message:
        return 'ok'

    # Отправка запроса в OpenAI
    gpt_response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': user_message}]
        }
    )

    reply_text = gpt_response.json()['choices'][0]['message']['content']

    # Отправка ответа в Telegram
    requests.post(
        TELEGRAM_API_URL,
        json={'chat_id': chat_id, 'text': reply_text}
    )

    return 'ok'
