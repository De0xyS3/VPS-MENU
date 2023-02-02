import requests
import time
import json
import random
import string

BOT_TOKEN = "youtoken"
CHAT_ID = "id"
B_SERVER_URL = 'http://192.168.0.18:8000'

def handle_telegram_command(text, chat_id):
    if text == "/token_generate":
        # Generate a new token
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Send the generated token to Telegram
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={token}")

        if response.status_code == 200:
            print(f"Token sent successfully: {token}")
            send_token_to_server_b(token)
        else:
            print("Error sending the token to Telegram")

def send_token_to_server_b(token):
    try:
        url = f'{B_SERVER_URL}/receive_token'
        headers = {'Content-Type': 'application/json'}
        payload = {'token': token}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print('Token sent to server B successfully.')
        else:
            print(f'Error sending token to server B. Response code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print('Error sending token to server B.', e)

def listen_to_telegram():
    # Get the last processed update_id
    last_update_id = None

    while True:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id}")
        if response.status_code == 200:
            updates = response.json()["result"]
            for update in updates:
                update_id = update["update_id"]
                if "message" in update:
                    message = update["message"]
                    chat_id = message["chat"]["id"]
                    if "text" in message:
                        text = message["text"]
                        handle_telegram_command(text, chat_id)

                last_update_id = update_id + 1

        time.sleep(2)

if __name__ == "__main__":
    listen_to_telegram()