from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import json

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
UserPicks = {}
UserPicks["userID"] = {}
pick = UserPicks["userID"]
class Events(APIView):
    def post(self, request, *args, **kwargs):

        #print(request.data)
        slack_message = request.data

        if type(request.data) != dict:
            slack_message = slack_message.dict()
            print(type(slack_message))
            if "payload" in slack_message:
                slack_message = json.loads(slack_message["payload"])

        print(type(slack_message))
        print(json.dumps(slack_message, sort_keys=True, indent=4))

        ## if the token in the message doesn't match out token then forbidden
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN :
                    return Response(status=status.HTTP_403_FORBIDDEN)

        #verification challenge
        if slack_message.get('type') == 'url_verification':  #
            return Response(data=slack_message,  #
                            status=status.HTTP_200_OK)  #

        #if the event is an interactive message response
        if slack_message.get('type') == 'interactive_message':
            choice = slack_message.get('actions')
            attachment = slack_message.get('original_message').get('attachments')
            callback = attachment[0]["callback_id"]

            pick[callback] = choice[0]["value"]
            print(UserPicks)


        return Response(status=status.HTTP_200_OK)
