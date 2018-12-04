from rest_framework import serializers
from . import models
from account import serializers as User_serializers
from Images import serializers as Image_serializers

class NotificationSerializer(serializers.ModelSerializer):

    creator = User_serializers.ListUserSerializer()
    to = User_serializers.ListUserSerializer()
    image = Image_serializers.SmallImageSerializer()

    class Meta:
        model = models.Notification
        fields = (
            'creator',
            'to',
            'notification_type',
            'image',
        )