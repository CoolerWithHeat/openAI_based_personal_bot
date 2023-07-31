import requests
import os

botToken = os.environ.get('BOT_TOKEN')
url = f"https://api.telegram.org/bot{botToken}/setWebhook?url=https://75d5-31-148-160-123.ngrok-free.app/FetchUpdates/"

request = requests.post(url)
print(request.text)