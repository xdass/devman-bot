import os
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
    params = None
    timestamp_to_request = None
    while True:
        try:
            import time
            time.sleep(60)
            print(params)
            response = requests.get(api_url, headers=headers, params=params)
            params = None
            if response.ok:
                json_response = response.json()
                status = json_response.get('status')
                if status == 'timeout':
                    print('Timeout!')
                    print(json_response)
                    timestamp_to_request = json_response.get('timestamp_to_request')

                    print(timestamp_to_request)
                    params = {'timestamp': timestamp_to_request}
                    timestamp_to_request = None
                elif status == 'found':
                    print(f'--->{json_response}')
                    # send_task_status(json_response)
                    params = None
            else:
                raise requests.HTTPError(response)
            # if timestamp_to_request:
            #     response = requests.get(
            #         api_url,
            #         headers=headers,
            #         params={'timestamp': timestamp_to_request})
            #     timestamp_to_request = None
            # else:
            # if timestamp_to_request:
            #     response = requests.get(api_url, headers=headers)
            #     if response.ok:
            #         json_response = response.json()
            #         print(json_response)
            #         timestamp_to_request = json_response.get('timestamp_to_request')
            #         status = json_response['status']
            #         if status == 'found':
            #             send_task_status(json_response)
            #         elif status == 'timeout':
            #             timestamp_to_request = response_json.get('timestamp_to_request')
            #             response = requests.get(
            #                 api_url,
            #                 headers=headers,
            #                 params={'timestamp': timestamp_to_request})
            #             timestamp_to_request = None
            #     else:
            #         raise requests.HTTPError(response)
        except requests.exceptions.ConnectionError as e:
            print(f"Не удалось установить соединение с сервером, пробуем ещё раз...")


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.getenv('bot_token')
    request_kwargs = {
        'proxy_url': 'socks5://',
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': '',
            'password': '',
        }
    }
    updater = Updater(token=bot_token, request_kwargs=request_kwargs)
    bot = updater.bot
    listen_polling()
