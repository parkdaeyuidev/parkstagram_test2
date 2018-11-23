from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from account import models as user_models

# Create your models here.
@python_2_unicode_compatible
class TimeStampModel(models.Model) :

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

@python_2_unicode_compatible
class Image(TimeStampModel) :

    """ Image Model """

    file = models.ImageField()
    locations = models.CharField(max_length=140)
    caption = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE,null=True, related_name='images')
    
    @property
    def like_count(self):
        return self.likes.all().count()

    def __str__(self):
        return '{} - {}'.format(self.locations, self.caption)

    class Meta:
        ordering = ['-created_at']

@python_2_unicode_compatible
class Comment(TimeStampModel) :

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='comments')

@python_2_unicode_compatible
class Like(TimeStampModel) :

    """ Like Model """
    
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='likes')