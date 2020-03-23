# Comics publisher

This script inform you about check status on devman task by send message to the telegram bot.<br>
If an error occurs while the bot is running, logger send info messages to telegram chat.

### How to install

1. You need devman api token.
2. Register telegram bot. This link helps you -> [How to register telegram bot](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/).
3. Create .env file and add token=devman_token, bot_token=your_bot_token and chat_id=your_chat_id.
To find chat_id , write message to telegram bot @userinfobot
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