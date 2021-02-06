from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User
from rooms.serializers import RoomSerializer
from rooms.models import Room

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data=ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            print(dir(user))
            return Response()
        else:
            return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(data= ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class FavsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data)

    def put(self, request):
        pk = request.data.get("pk",None)
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