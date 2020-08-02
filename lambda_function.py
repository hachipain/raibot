import os
import sys
import requests
import json
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from linebot.exceptions import InvalidSignatureError
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
chaplus_api_key = os.getenv('CHAPLUS_API_KEY', None)

if channel_secret is None:
    logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

if channel_access_token is None:
    logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

if chaplus_api_key is None:
    logger.error('Specify CHAPLUS_API_KEY as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def getUserName(user_id):
    url = f'https://api.line.me/v2/bot/profile/{user_id}'

    user_profile = requests.get(url,
        headers={
            'Authorization' :  f'Bearer {channel_access_token}',
        })
    json_data = user_profile.json()
    user_name = json_data['displayName']

    return user_name

def getChaplusMessage(mes, username):
    dialogue_option = {
        'utterance': mes,
        'username': username,
        'agentState': {
            'agentName': 'らい',
            'age': '20歳',
            'tone': 'kansai'
        }
    }

    chaplusUrl = f'https://www.chaplus.jp/v1/chat?apikey={chaplus_api_key}'

    resp = requests.post(chaplusUrl,
                         data=json.dumps(dialogue_option),
                         headers={'Content-Type': 'application/json'})

    json_data = resp.json()
    answer = json_data['bestResponse']['utterance']

    return answer


def lambda_handler(event, context):
    signature = event["headers"]["X-Line-Signature"]
    body = event["body"]
    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 403,
                  "headers": {},
                  "body": "Error"}

    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        user_id = line_event.source.user_id
        user_name = getUserName(user_id)
        # text = line_event.message.text
        text = getChaplusMessage(mes=line_event.message.text,username=user_name)
        line_bot_api.reply_message(line_event.reply_token,
                                   TextMessage(text=text))

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        return error_json
    except InvalidSignatureError:
        return error_json

    return ok_json
