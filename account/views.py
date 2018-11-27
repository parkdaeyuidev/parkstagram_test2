#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status
# Create your views here.

class ExploreUsers(APIView):
    
    def get(self, request, format=None):
        
        last_five = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.UserSerializer(last_five, many=True)
        
        return Response(serializer.data)

class FollowerUser(APIView):

    def post(self,request,user_id, format=None):
        
        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
