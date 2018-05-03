import nflgame
from slackclient import SlackClient
import time
from django.conf import settings
import nflgame
import json

SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
print(SLACK_BOT_USER_TOKEN)
sc = SlackClient(SLACK_BOT_USER_TOKEN)
channels = sc.api_call("groups.list", exclude_archived=1)
print(json.dumps(channels, sort_keys=True, indent=4))


wk_num = 9
game_num = 1
class Getgames:
    channel_id = "GAHQYH5FZ"
    sc.api_call("chat.postMessage", channel=channel_id, text="Week 1: Game" + str(wk_num), attachments=[
        {
            "text": "DET at CAR 1PM EST",
            "fallback": "Make Your Pick!",
            "callback_id": "wk" + str(wk_num) + "-g" + str(game_num),
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "DET",
                    "type": "button",
                    "value": "DET",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Yes, pick Detroit!",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                },
                {
                    "name": "game",
                    "text": "CAR",
                    "type": "button",
                    "value": "CAR",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Yes, pick Carolina!",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }

            ]
        },
        {
            "text": "NE at DEN 1PM EST",
            "fallback": "Make Your Pick!",
            "callback_id": "wk" + str(wk_num) + "-g" + str(2),
            "color": "red",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "DEN",
                    "type": "button",
                    "value": "DEN",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Yes, pick Denver!",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                },
                {
                    "name": "game",
                    "text": "NE",
                    "type": "button",
                    "value": "NE",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Yes, pick New England!",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }

            ]
        }
    ])

    if sc.rtm_connect():
        print("Connected!")
        #while True:
            #print(sc.rtm_read())
            #time.sleep(1)

    else:
        print("Connection failed. Invalid Slack token or bot ID")