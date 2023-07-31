import os, PersonalAI, re, requests
from telethon.sync import TelegramClient
from telethon import connection
from telethon.sessions import StringSession
from telethon import events
from telethon.tl import types

locationDetails = {
    "University": {'latitude':41.320566, 'longitude': 69.261249},
    "Residential": {'latitude': 41.328892, 'longitude': 69.256050},
}

proxy_host = "proxy.server"
proxy_port = 3128
proxy_type = "http"
proxy = connection.ConnectionHttp(proxy_host, proxy_port, dc_id=1, loggers=None)


def retrieve_and_remove_keywords(text, keywords):

    keywords_found = []
    text_without_keywords = text
    
    for keyword in keywords:

        matches = re.findall(keyword, text_without_keywords, re.IGNORECASE)
        
        if matches:

            keywords_found.extend(matches)
            

            text_without_keywords = re.sub(keyword, '', text_without_keywords, flags=re.IGNORECASE)
    
    return keywords_found, text_without_keywords

async def Location_Asked(message):
    response = message.lower()
    locationKeyword = 'Residential' if ('abay' in response or '16A' in response) else "University" if ('alisher navoi' in response) or ('webster' in response) else None
    return locationKeyword

async def GetLocation(chat_id, latitude, longitude, title=None):
    geo_point = types.InputMediaGeoPoint(
        geo_point=types.InputGeoPoint(
            lat=latitude,
            long=longitude,
            accuracy_radius=1 
        ),
    )
    return geo_point


def GetConnectionString():
    try:
        with open("session_string.txt", "r") as f:
            session_string = f.read()
            return session_string
    except FileNotFoundError:
        print("Error: session_string.txt file not found.")
        return None

bot_token = os.environ.get('BOT_TOKEN')
api_hash = os.environ.get('API_HASH')
api_id = os.environ.get('API_ID')
session_string = GetConnectionString()

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def delete_message(message_id, chat_id, bot):
    response = await bot.delete_messages(chat_id, message_id)

async def respondBack(response, chat_id, bot):
    response = await bot.send_message(chat_id, "...loading, it take a couple of seconds depeding on server load.")
    return response.id

def getLocationIndex(locationSign):
    if locationSign == 'University':
        return locationDetails.get('University', None)
    elif locationSign == 'Residential':
        return locationDetails.get('Residential', None)

@client.on(events.NewMessage)
async def on_message(event):

    if event.is_private and not event.message.out:
        chat_id = event.chat_id
        message_text = event.text

        loadingResponse = await respondBack("loading...", chat_id, client)

        async with client.action(event.chat_id, "typing"):

            try:
                AI_response = PersonalAI.Request_Question(message_text)
                await delete_message(loadingResponse, chat_id, client)
                await event.respond(AI_response)
                SpecificLocation = await Location_Asked(AI_response)
                if SpecificLocation:
                    parameters = getLocationIndex(SpecificLocation)
                    askedLocation = await GetLocation(chat_id, **parameters, )
                    locationResponse = await client.send_message(chat_id, file=askedLocation, message="This is the location")
                    await client.send_message(chat_id, reply_to=locationResponse.id, message=f"This is the location of his {'apartment' if SpecificLocation =='Residential' else 'University, Webster'}")
            except:
                await delete_message(loadingResponse, chat_id, client)
                await event.respond("Sorry server is down, please come later to know more about Mansur, many people trying to get to know about him, request limits exceeded.")



def main():
    if session_string:

        client.start(bot_token=bot_token)
        client.run_until_disconnected()

if __name__ == "__main__":
    main()