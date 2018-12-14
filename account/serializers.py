from rest_framework import serializers
from . import models
from Images import serializers as Image_serializers

class UserSerializer(serializers.ModelSerializer) :

    images = Image_serializers.ImageSerializer(many=True)
    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'nickname',
            'name',
            'website',
            'bio',
            'followers_count',
            'following_count',
            'post_count',
            'images'
        )

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'nickname',
            'name'
        )