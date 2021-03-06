import os
import json
import requests
from datetime import datetime
import tweepy

api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
token = os.getenv('TWITTER_ACCESS_TOKEN')
token_secret = os.getenv('TWITTER_TOKEN_SECRET')
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth)

months = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

def tweet(text):
    print(f'tweet:{text}')
    response = api.update_status(text)

def lambda_handler(event, context):
    text = None
    share = False
    response = requests.get('https://raw.githubusercontent.com/GavinPalmer1984/rasa_bots/master/politician_bot/domain.yml')
    for line in response.text.split("\n"):
        parts = line.split('  utter_journal_entry_')
        if len(parts) > 1:
            print(f'check journal entry:{line}')
            date_parts = parts[1].split('_')
            month = date_parts[0]
            day = date_parts[1]
            year = date_parts[2].split(':')[0]
            date = datetime(int(year), months[month.lower()], int(day))
            now = datetime.now()
            if now.year == date.year and now.month == date.month and now.day == date.day:
                share = True
        elif share:
            text = line.split('  - text: ')[1]
            tweet(text)
            share = False

    return {
        'statusCode': 200,
        'body': json.dumps(text)
    }

lambda_handler(None, None)
