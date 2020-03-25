# Comics publisher

This script inform you about check status on devman task by send message to the telegram bot.<br>
If an error occurs while the bot is running, logger send info messages to telegram chat.

### How to install

1. You need devman api token.
2. Register telegram bot and save token. This link helps you -> [How to register telegram bot](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/).
3. Create .env file and add next lines:
* ```DVMN_TOKEN=devman_token``` - your token for dvmn.org
* ```TELEGRAM_TOKEN=your_bot_token``` - your token of telegram bot
* ```CHAT_ID=your_chat_id``` - your telegram chat_id. To find chat_id , write message to telegram bot @userinfobot
* ```PROXY=proxy_addr``` - proxy server address (if you use proxy fill this variable)
* ```PROXY_LOGIN``` - proxy login (if you use proxy fill this variable)
* ```PROXY_PASSWORD``` - proxy password (if you use proxy fill this variable)
<br> 
4. Install dependencies (written below)

# Deploy Heroku
See instructions -> [How to deploy on heroku](https://devcenter.heroku.com/articles/git)

Note: This script using SOCKS5 Proxy, because from Russia access to telegram is blocked.
#### Proxy settings
[You can buy proxies here](https://proxy6.net)
```
    request_kwargs = {
        'proxy_url': 'socks5://proxy_adress',
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': 'username',
            'password': 'password',
        }
    }
```
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
### Program output example
```
python main.py
```
### Example
<img src="https://i.ibb.co/qx4L0fS/bot-logger.png" alt="bot-logger" border="0"></a><br />
### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).