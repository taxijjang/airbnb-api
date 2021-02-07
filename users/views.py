import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import UserSerializer
from .models import User
from rooms.models import Room

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action =="retireve":
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data=UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            print(dir(user))
            return Response(data=UserSerializer(user).data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(data=UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encode_jwt = jwt.encode(
            {'id': user.pk}, settings.SECRET_KEY, algorithm='HS256')
        return Response(data={'token': encode_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)