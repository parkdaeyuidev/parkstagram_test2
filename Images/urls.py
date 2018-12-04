from django.conf.urls import url
from django.urls import path
from . import views
from . import stibee

urlpatterns = [
    path('',views.ListAllImages.as_view(),name='all_images'),
    # path('api/comments/',views.ListAllComment.as_view(),name='all_comments'),
    # path('api/likes/',views.ListAllLikes.as_view(),name='all_likes'),
    path('feed/',views.Feed.as_view(),name="feed"),
    path('like/<int:image_id>/',views.LikeImage.as_view(),name='like_image'), #좋아요
    path('unlike/<int:image_id>/',views.UnLikeImage.as_view(),name='unlike_image'), #좋아요취소
    path('comment/<int:image_id>/',views.CommentOnImage.as_view(),name='comment_image'), #댓글생성
    path('<int:comment_id>/comment/',views.Comment.as_view(),name='comment'),
    path('search/',views.Search.as_view(),name='search'),
  
    # 스티비_테스트
    path('stibee/', stibee.StibeeTestView.as_view(), name="stibee_test"),
] 