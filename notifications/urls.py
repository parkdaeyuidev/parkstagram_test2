from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Notifications.as_view(),name="notifications"),
] 