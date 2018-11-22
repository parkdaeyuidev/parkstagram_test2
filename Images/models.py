from django.db import models
from account import models as user_models

# Create your models here.

class TimeStampModel(models.Model) :

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Image(TimeStampModel) :

    """ Image Model """

    file = models.ImageField()
    locations = models.CharField(max_length=140)
    caption = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE,null=True)
    

class Comment(TimeStampModel) :

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='comments')

class Like(TimeStampModel) :

    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='likes')
