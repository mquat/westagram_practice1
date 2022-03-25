import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from .models import User

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
            #기존 이메일과 중복일 경우 
            if User.objects.filter(email = data['email']):
                return JsonResponse({"message":"ALREADY_EXISTS"}, status=400)

            #양식에 맞지 않는 이메일일 경우
            if not re.match(REGEX_EMAIL, data['email']):
                return JsonResponse({"message":"INVALID_EMAIL"}, status=400)

            #양식에 맞지 않는 비밀번호인 경우 
            if not re.match(REGEX_PASSWORD, data['password']):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)

            #비밀번호 암호화 
            password = data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = hashed_password,
                phone_number = data['phone_number']
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)   
        except KeyError:
            return JsonResponse({"messsage":"KEYERROR"}, status=400)

class SignInView(View):
    def post(self,request):
        try: 
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            #비번 인증 logic 추가 및 에러 return 
            if not User.objects.filter(email = email):
                return JsonResponse({"message":"INVALID_USER"}, status=401)

            hashed_password  = User.objects.get(email = email).password
            checked_password = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            if not checked_password:
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)
            
            #JWT 발행 및 전송 
            payload      = User.objects.get(email = email).id
            access_token = jwt.encode({"id" : payload}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
            return JsonResponse({
                "message": "SUCCESS",
                "token" : access_token
                }, status = 200)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

     

            
