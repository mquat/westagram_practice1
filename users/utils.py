import json
import jwt

from django.http import JsonResponse

from .models import User 
from practice.settings import SECRET_KEY, ALGORITHM

def signin_decorator(func):
        def wrapper(self, request, *args, **kwargs):
            try: 
                # 얘는 없애야 함! data = json.loads(request.body)
                access_token = request.headers.get('Authorization') 
                payload  = jwt.decode(access_token, SECRET_KEY, algorithms = ALGORITHM)
                #request에 user라는 속성을 내가 추가한 것 
                request.user = User.objects.get(id = payload['id'])

            except jwt.exceptions.DecodeError:
                return JsonResponse({"message" : "TOKEN_ERROR"}, status = 400)
            except User.DoesNotExist:
                return JsonResponse({"message" : "INVALID_USER"}, status = 400)
            
            return func(self, request)

        return wrapper
            
        