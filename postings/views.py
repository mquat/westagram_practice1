import json

from django.http import JsonResponse
from django.views import View

from users.models import User
from users.utils  import signin_decorator

from .models import Image, Post, Comment

class PostingView(View):
    @signin_decorator
    def post(self, request):
        try: 
            data = json.loads(request.body)
            user    = request.user
            content = data['content'] 
            images  = data['image_url']

            post = Post.objects.create(
                user    = user, 
                content = content
            )

            for image in images:
                Image.objects.create(
                    post      = post,
                    image_url = image
                )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "NO_IMAGE_OR_CAPTION"}, status = 404) 
    
    @signin_decorator
    def get(self, request):
        posts = Post.objects.all()
        result = [{
            "postId"      : post.id,
            "profileName" : post.user.name,
            "profileUrl"  : 'https://hhspress.org/wp-content/uploads/2020/05/2-24435_red-angry-birds-red-angry-birds-png-transparent.png',
            "feedContent" : post.content,
            "contentUrl"  : [image.image_url for image in post.image_set.all()],
            
            #for test: client측으로부터 받은 mock data
            "commentList" : [{
                "id" : 1,
                "userName": "minju",
                "content" : "위코드 화이팅!! Mock data 작업 너무 재밌당",
                "isLiked" : True
            }]
        } for post in posts]

        return JsonResponse({"message" : result}, status = 200)

class CommentsView(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)
        user       = request.user
        post       = data['post']
        created_at = data['created_at']
        comment    = data['comment']

        Comment.objects.create(
            post       = post,
            user       = user,
            comment    = comment,
            created_at = created_at
        )

        return JsonResponse({"message" : "SUCCESS"}, status = 201)
    
    @signin_decorator
    def get(self, request):
        comments = Comment.objects.all()
        result = [{
            "user"       : comment.user.name,
            "comment"    : comment.comment,
            "created_at" : comment.created_at
            } for comment in comments]

        return JsonResponse({"message" : result}, status = 200)
        