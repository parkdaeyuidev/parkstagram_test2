from rest_framework import serializers
from . import models
from account import models as user_models

class CountImageSerializer(serializers.ModelSerializer) :

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
        )

class FeedUserSerializer(serializers.ModelSerializer) :
    
    class Meta:
        model = user_models.User
        fields = (
            'nickname',
            'profile_image'    
        )

class CommentSerializer(serializers.ModelSerializer):
    
    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator'
        )

class LikeSerializer(serializers.ModelSerializer):

    #image = ImageSerializer(read_only=True)

    class Meta:
        model = models.Like
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'creator',
            'file',
            'caption',
            'locations',
            'comments',
            'like_count',
            'likes',
            'created_at',
            'updated_at',
        )

class SmallImageSerializer(serializers.ModelSerializer):

    """User for Notification"""

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file'
        )

class InputImageSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = models.Image
        fields = (
            'file',
            'locations',
            'caption',
        )
