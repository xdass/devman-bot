import os
import time
import traceback
import logging
import requests
from telegram.ext import Updater
from dotenv import load_dotenv


class SendStatusException(Exception):
    pass


class BotLogsHandler(logging.Handler):

    def __init__(self, token):
        self.updater = Updater(token=token)
        self.bot = self.updater.bot
        super().__init__()

    def emit(self, record):
        chat_id = os.getenv('CHAT_ID')
        log_entry = self.format(record)
        self.bot.send_message(chat_id=chat_id, text=log_entry)


def send_task_status(json_body):
    chat_id = os.getenv('CHAT_ID')
    base_url = "https://dvmn.org"
    attempts = json_body['new_attempts']
    try:
        for attempt in attempts:
            lesson_title = attempt['lesson_title']
            lesson_url = attempt['lesson_url']
            is_negative = attempt['is_negative']
            if is_negative:
                message = f"""Была проверена задача \"{lesson_title}\"
                    В задаче имеются ошибки. Посмотреть {base_url + lesson_url}"""
            else:
                message = f"""Была проверена задача \"{lesson_title}\"
                    Задача успешно решена!"""
            bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        raise SendStatusException(e)


def listen_polling():
    token = os.getenv('DVMN_TOKEN')
    connect_attempts = 3
    api_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {token}'
    }
    params = None
    while True:
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=95)
            response.raise_for_status()
            json_response = response.json()
            status = json_response.get('status')
            if status == 'timeout':
                params = {'timestamp': json_response.get('timestamp_to_request')}
            elif status == 'found':
                send_task_status(json_response)
                params = {'timestamp': json_response.get('last_attempt_timestamp')}
        except requests.exceptions.ConnectionError as e:
            connect_attempts -= 1
            print(f"Не удалось установить соединение с сервером, пробуем ещё раз...")
            if connect_attempts == 0:
                print(f"Не удалось установить соединение с сервером, таймаут 30 секунд.")
                time.sleep(30)
        except requests.exceptions.ReadTimeout as e:
            print(f"Ответ от сервера не получен, пробуем ещё раз...")
        except SendStatusException:
            logger.info(f"Бот упал с ошибкой:")
            logger.info(traceback.format_exc())


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv('TELEGRAM_TOKEN')
    proxy_url = os.getenv('PROXY')
    proxy_login = os.getenv('PROXY_LOGIN')
    proxy_password = os.getenv('PROXY_PASSWORD')

    logger = logging.getLogger("notify_bot")
    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogsHandler(bot_token))

    request_kwargs = {
        'proxy_url': proxy_url,
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': proxy_login,
            'password': proxy_password,
        }
    }
    updater = Updater(token=bot_token)
    bot = updater.bot
    logger.info("Бот запущен!")
    listen_polling()
