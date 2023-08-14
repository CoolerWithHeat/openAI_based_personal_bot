import requests
import os

botToken = os.environ.get('BOT_TOKEN')
url = f"https://api.telegram.org/bot{botToken}/setWebhook?url=https://telegram-botserver-3fccedd8685f.herokuapp.com/FetchUpdates/"

request = requests.post(url)
print(request.text)