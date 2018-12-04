from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('people/',views.ExploreUsers.as_view(),name='explore_users'),
    path('<int:user_id>/follow/',views.FollowerUser.as_view(),name='follow_user'),
     path('user/search/',views.SearchUser.as_view(),name='user_search'),
    path('user/<nickname>/',views.UserProfile.as_view(),name='user_profile'),
    path('user/<nickname>/followers/',views.UserFollowers.as_view(),name='user_followers'),
    path('user/<nickname>/followings/',views.UserFollowings.as_view(),name='user_followings'),
   
]
