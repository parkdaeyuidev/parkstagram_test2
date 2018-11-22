from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('api/images/',views.ListAllImages.as_view(),name='all_images'),
    path('api/comments/',views.ListAllComment.as_view(),name='all_comments'),
    path('api/likes/',views.ListAllLikes.as_view(),name='all_likes'),
]