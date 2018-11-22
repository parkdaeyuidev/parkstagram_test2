from rest_framework import serializers
from . import models

class CommentSerializer(serializers.ModelSerializer):
    
    # image = ImageSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    #image = ImageSerializer(read_only=True)

    class Meta:
        model = models.Like
        fields = '__all__'



class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)

    class Meta:
        model = models.Image
        fields = (
            'id',
            'creator',
            'file',
            'caption',
            'locations',
            'comments',
            'likes',
            'created_at',
            'updated_at',
        )

