#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status
# Create your views here.

class ExploreUsers(APIView):
    
    def get(self, request, format=None):
        
        last_five = models.User.objects.all()[:5]
        serializer = serializers.UserSerializer(last_five, many=True)
        
        return Response(serializer.data)