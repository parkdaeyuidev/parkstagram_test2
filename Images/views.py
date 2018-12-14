# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models,serializers
from account import models as user_models,serializers as user_serializers
from rest_framework import status
from notifications import views as notifications_views

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


        my_images = user.images.all()[:2]

        for image in my_images:

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

    def get(self,request, image_id, format=None):
         
         likes = models.Like.objects.filter(image__id=image_id)

         like_creators_ids = likes.values('creator_id')

         users = user_models.User.objects.filter(id__in=like_creators_ids)

         print(users)
         serializer = user_serializers.ListUserSerializer(users, many=True)

         return Response(data=serializer.data, status=status.HTTP_200_OK)

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

            notifications_views.create_notification(user,found_image.creator, 'Like', found_image)

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
            notifications_views.create_notification(user,found_image.creator,'comment',found_image,request.data['message'])
        
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

class Search(APIView):
    def get(self,request,foramt=None):

        hashtags = request.query_params.get('hashtags',None)

        if hashtags is not None:

            hashtags = hashtags.split(",")
            
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else :

            return Response(status=status.HTTP_400_BAD_REQUEST)

class ModerateComment(APIView):

    def delete(self, request,image_id, comment_id, format=None):

        user = request.user

        # try:
        #     image = models.Image.objects.get(id=image_id,creator=user)
        # except: models.Image.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            comment_to_delete = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):

        user = request.user
        
        try:
            single_image = models.Image.objects.get(id=image_id)            
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(single_image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(creator=user)

            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):

        user = request.user

        image = self.find_own_image(image_id, user)

        if image is None:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)








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