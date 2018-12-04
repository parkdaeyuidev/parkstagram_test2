from django.db import models
from account import models as user_models
from Images import models as image_models
# Create your models here.

class Notification(image_models.TimeStampModel) :

    TYPE_CHOICES = (
        ('Like','like'),
        ('comment','Comment'),
        ('follow','Follow'),
    )

    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name='creator')
    to = models.ForeignKey(user_models.User, on_delete=models.CASCADE,related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, on_delete=models.CASCADE, null=True,blank=True)
    comment = models.TextField(blank=True,null=True)