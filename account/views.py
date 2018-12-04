#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status
from notifications import views as notifications_views
# Create your views here.

class ExploreUsers(APIView):
    
    def get(self, request, format=None):
        
        last_five = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(last_five, many=True)
        
        return Response(serializer.data)

class FollowUser(APIView):

    def post(self,request,user_id, format=None):
        
        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user.save()

        notifications_views.create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)

class UnFollowUser(APIView):

    def post(self,request,user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)
        user.save()

        return Response(status=status.HTTP_200_OK)

class UserProfile(APIView):

    def get(self, request, nickname, format=None):
        try:
            found_user = models.User.objects.get(nickname=nickname)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(found_user)

        return Response(data = serializer.data, status=status.HTTP_202_ACCEPTED)

        
class UserFollowers(APIView):

    def get(self, request, nickname, format=None):

        try:
            found_user = models.User.objects.get(nickname=nickname)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()
        
        serializer = serializers.ListUserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

class UserFollowings(APIView):

    def get(self, request, nickname, format=None):

        try:
            found_user = models.User.objects.get(nickname=nickname)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followings = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_followings, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

class SearchUser(APIView):

    def get(self, request, format=None):

        nickname = request.query_params.get('nickname',None)

        if nickname is not None:

            users = models.User.objects.filter(nickname__istartswith=nickname)

            serializer = serializers.ListUserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)