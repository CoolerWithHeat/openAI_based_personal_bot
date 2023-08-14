import requests
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url=https://telegram-botserver-3fccedd8685f.herokuapp.com/FetchUpdates/"

request = requests.post(url)
print(request.text)