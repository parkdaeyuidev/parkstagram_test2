from django.views import View
import requests
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.response import Response
from . import models,serializers
import json

class StibeeTestView(APIView):
    
    def post(self, request,format=None):
        print("hello")
        try:
            url = 'https://api.stibee.com/v1/lists/21645/subscribers'
            headers = {
                'Content-Type': 'application/json',
                'AccessToken' : 'e2ef86b58ae3cc36d9d1e56eb299bdfb5781d019f1f4c734c569a729458d8798d4571fb1986860cef37caa209684aa1bcc88a46c7b98f5867ee677c068f06f51',
            }
            data = {
                "eventOccuredBy": "SUBSCRIBER",
                "confirmEmailYN": "N",
                "groupIds" : [
                    "9146"
                ],
                "subscribers": [
                    {
                        "email": "parkdaeyuidev@naver.com",
                        "name": "박대윤",
                    },
                ]
            }
            response = requests.post(
                url,
                data = json.dumps(data),
                headers = headers,  
            )
            print(json.dumps(data))
            print("this")
            print(response.text)
            return Response(status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_304_NOT_MODIFIED)        