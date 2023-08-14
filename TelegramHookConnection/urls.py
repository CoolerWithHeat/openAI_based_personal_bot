from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, os, asyncio
from . import PersonalAI
from telegram import Bot



locationDetails = {
    "University": {'latitude':41.320566, 'longitude': 69.261249},
    "Residential": {'latitude': 41.328892, 'longitude': 69.256050},
}

ConnectionToken = os.environ.get('BOT_TOKEN')
developersChat = 6089655614

def getLocationIndex(locationSign):
    if locationSign == 'University':
        return locationDetails.get('University', None)
    elif locationSign == 'Residential':
        return locationDetails.get('Residential', None)

async def Location_Asked(message):
    response = message.lower()
    locationKeyword = 'Residential' if ('abay' in response or '16A' in response) else "University" if ('alisher navoi' in response) or ('webster' in response) else None
    return locationKeyword

async def SendResponseBack(chat_id, message):
    bot = Bot(token=ConnectionToken)
    alertMessage = await bot.send_message(chat_id, text="loading... it may take couple of seconds depending on server load.")
    AI_response = PersonalAI.Request_Question(message)

    await bot.send_message(chat_id, text=AI_response)
    await bot.delete_message(chat_id, alertMessage.id)

    SpecificLocation = await Location_Asked(AI_response)
    if SpecificLocation:
        parameters = getLocationIndex(SpecificLocation)
        locationMessage = await bot.send_location(chat_id=chat_id, **parameters)
        await bot.send_message(chat_id, reply_to_message_id=locationMessage.id, text=f"here is the location of his {'apartment' if (SpecificLocation.lower() == 'residential') else 'university, Webster'}")

def Parse_Telegram_Hook_Input(DictData):

    BaseData = DictData.get('message', None)
    senderDetailsBase = BaseData['from']
    
    # Main Details Needed For Response Down Below
    senderName = senderDetailsBase.get('first_name', None)
    RequestedMessage = BaseData['text']
    chatID = BaseData['chat']['id']
    
    return {"chat_id": chatID, "senderName": senderName, "message":RequestedMessage}


@csrf_exempt
def GetTelegramUpdate(request):
    TelegramResponse = json.loads(request.body)
    processed_data = Parse_Telegram_Hook_Input(TelegramResponse)
    asyncio.run(SendResponseBack(processed_data['chat_id'], processed_data['message']))
    return JsonResponse({"data_accepted": True})


async def ConsultingAlert(rawData):
    bot = Bot(token=ConnectionToken)
    sender = rawData.get('sender', None)
    email = rawData.get('email', None)
    consultancyType = rawData.get('selectedService', None)
    await bot.send_message(developersChat, text=f"A new consulting has been appointed!\n{sender} registered for {consultancyType}\nclient's contact: {email}")

@csrf_exempt
def RegisterConsulting(request):
    arrivedData = json.loads(request.body)
    from_consulting = arrivedData.get("consulting", None)
    if from_consulting:
        asyncio.run(ConsultingAlert(arrivedData)) 
    return JsonResponse({"data_accepted": True})

urlpatterns = [

    path('admin/', admin.site.urls),
    path("FetchUpdates/", GetTelegramUpdate),
    path("consulting-registration/", RegisterConsulting),
    
]