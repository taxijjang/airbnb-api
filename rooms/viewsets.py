from rest_framework import viewsets
from .models import Room
from .serializers import RoomSerializer, BigRoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer
