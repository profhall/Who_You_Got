from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import nflgame
import json

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
UserPicks = {}
pick = ""

class Events(APIView):
    def post(self, request, *args, **kwargs):
        global UserPicks, pick
        #print(request.data)
        slack_message = request.data

        if type(request.data) != dict:
            slack_message = slack_message.dict()
            print(type(slack_message))
            if "payload" in slack_message:
                slack_message = json.loads(slack_message["payload"])

        #print(type(slack_message))
        #print(json.dumps(slack_message, sort_keys=True, indent=4))

        ## if the token in the message doesn't match out token then forbidden
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN :
                    return Response(status=status.HTTP_403_FORBIDDEN)

        #verification challenge
        if slack_message.get('type') == 'url_verification':  #
            return Response(data=slack_message,  #
                            status=status.HTTP_200_OK)  #

        #needed to check if user has already made a decision,
        #this is to make sure that every even doesnt create an empty dictionary
        if "user" in slack_message :
            user = slack_message["user"]["name"]
            if user not in UserPicks:
                UserPicks[user] = {}
                pick = UserPicks[user]

        #if the event is an interactive message
        if slack_message.get('type') == 'interactive_message':
            choice = slack_message.get('actions')
            weekNgame = slack_message["callback_id"]
            pick[weekNgame] = choice[0]["value"]
            print(UserPicks)
            print(pick)


        return Response(status=status.HTTP_200_OK)

    def writeToFile(self, data):
        # save to file:
        with open('/picks/team_picks.json', 'w') as f:
            json.dump(data, f)
