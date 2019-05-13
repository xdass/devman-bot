import os
import time
import requests
from telegram.ext import Updater
from dotenv import load_dotenv


def send_task_status(json_body):
    chat_id = os.getenv('chat_id')
    base_url = "https://dvmn.org"
    lesson_title = json_body['new_attempts'][0]['lesson_title']
    lesson_url = json_body['new_attempts'][0]['lesson_url']
    is_negative = json_body['new_attempts'][0]['is_negative']
    if is_negative:
        message = f"Была проверена задача \"{lesson_title}\"\n\n Задача успешно решена!"
    else:
        message = f"Была проверена задача \"{lesson_title}\"" \
            f"\n\n В задаче имеются ошибки. Посмотреть {base_url + lesson_url}"
    bot.send_message(chat_id=chat_id, text=message)


def listen_polling():
    token = os.getenv('token')
    api_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {token}'
    }
    start_timestamp = time.time()
    params = {'timestamp': start_timestamp}
    while True:
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=95)
            if response.ok:
                json_response = response.json()
                status = json_response.get('status')
                response_time = time.time()
                if status == 'timeout':
                    params = {'timestamp': response_time}
                elif status == 'found':
                    send_task_status(json_response)
                    params = {'timestamp': response_time}
            else:
                raise requests.HTTPError(response)
        except requests.exceptions.ConnectionError as e:
            print(f"Не удалось установить соединение с сервером, пробуем ещё раз...")
        except requests.exceptions.ReadTimeout as e:
            print(f"Ответ от сервера не получен, пробуем ещё раз...")


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv('bot_token')
    proxy_url = os.getenv('proxy')
    proxy_login = os.getenv('proxy_login')
    proxy_password = os.getenv('proxy_password')
    request_kwargs = {
        'proxy_url': proxy_url,
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': proxy_login,
            'password': proxy_password,
        }
    }
    updater = Updater(token=bot_token, request_kwargs=request_kwargs)
    bot = updater.bot
    listen_polling()
