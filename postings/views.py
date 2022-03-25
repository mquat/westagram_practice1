import json

from django.http import JsonResponse
from django.views import View

from users.models import User
from users.utils  import signin_decorator

from .models import Image, Post

class PostingView(View):
    @signin_decorator
    def post(self, request):
        try: 
            data = json.loads(request.body)
            caption = data['caption'] 
            images  = data['images']

            post = Post.objects.create(user = request.user, caption = caption)
            for image in images:
                Image.objects.create(
                    post      = post,
                    image     = image
                )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "NO_IMAGE_OR_CAPTION"}, status = 404) 
    
    @signin_decorator
    def get(self, request):
        posts = Post.objects.filter(user = request.user)
        result = [{
            "user"       : post.user.name,
            "caption"    : post.caption,
            "images"     : [image.image for image in post.image_set.all()],
            "created_at" : post.created_at
        } for post in posts]

        return JsonResponse({"message" : result}, status = 200)
