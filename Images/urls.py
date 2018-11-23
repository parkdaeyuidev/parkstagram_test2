from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('images/',views.ListAllImages.as_view(),name='all_images'),
    # path('api/comments/',views.ListAllComment.as_view(),name='all_comments'),
    # path('api/likes/',views.ListAllLikes.as_view(),name='all_likes'),
    path('feed/',views.Feed.as_view(),name="feed"),
    path('like/<int:image_id>/',views.LikeImage.as_view(),name='like_image'), #좋아요
    path('comment/<int:image_id>/',views.CommentOnImage.as_view(),name='comment_image'), #댓글생성
    path('<int:comment_id>/comment/',views.Comment.as_view(),name='comment'),
] 