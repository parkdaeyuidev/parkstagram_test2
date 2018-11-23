from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('people/',views.ExploreUsers.as_view(),name='explore_users'),
] 