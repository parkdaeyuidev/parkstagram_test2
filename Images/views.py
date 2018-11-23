# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models,serializers
from rest_framework import status


#내 아이디에 팔로되어있는 유저들의 이미지를 출력
class Feed(APIView) :

    def get(self, request, format=None):
        
        user = request.user
        following_users = user.following.all()

        image_list = []

        for following_user in following_users:

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        sorted_list = sorted(image_list, key=get_key, reverse=True)
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)

def get_key(image):
    return image.created_at

class ListAllImages(APIView):

    def get(self, request, format=None):

        all_images = models.Image.objects.all()
        serializer = serializers.ImageSerializer(all_images, many=True)

        return Response(data=serializer.data)

class LikeImage(APIView):

    def post(self,request,image_id, format=None) :

        user = request.user

        try:

            found_image = models.Image.objects.get(id=image_id)

        except models.Image.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        try:

            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            
            return Response(status=status.HTTP_304_NOT_MODIFIED) #204 is no content

        except models.Like.DoesNotExist:

            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)

class UnLikeImage(APIView):
    
    def delete(self,request,image_id, format=None) :

        user = request.user

        try:

            found_image = models.Image.objects.get(id=image_id)

        except models.Image.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()

            return Response(status=status.HTTP_202_ACCEPTED)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)        
      

class CommentOnImage(APIView) :
    
    def post(self,request,image_id, format=None) :

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid() :

            serializer.save(creator=user, image=found_image)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Comment(APIView):

    def delete(self, request,comment_id, format=None):
        
        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class ListAllComment(APIView):

#     def get(self, request, format=None):

#         user_id = request.user.id

#         # all_comment = models.Comment.objects.all()
#         all_comment = models.Comment.objects.filter(creator=user_id)

#         serializer = serializers.CommentSerializer(all_comment, many=True)

#         return Response(data=serializer.data)

# class ListAllLikes(APIView):

#     def get(self, request, format=None):

#         all_likes = models.Like.objects.all()

#         serializer = serializers.LikeSerializer(all_likes, many=True)

#         return Response(data=serializer.data)