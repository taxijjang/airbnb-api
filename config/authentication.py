import jwt
from django.conf import settings
from users.models import User
from rest_framework import authentication



class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHENTICATION")
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ")
            decode = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            pk = decode.get("id")
            user = User.objects.get(pk=pk)
            return (user, None)
        except (ValueError,jwt.exceptions.DecodeError,User.DoesNotExist) :
            return None
