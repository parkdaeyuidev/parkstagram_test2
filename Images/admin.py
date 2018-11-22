from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin) :
    
    list_display = (
        'creator',
        'file',
        'locations',
        'caption',
    )

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin) :
    
    list_display = (
        'creator',
        'image',
    )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin) :

    list_display = (
    'creator',
    'image',
    'message',
    )
    
