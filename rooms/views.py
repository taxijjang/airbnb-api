from rest_framework.generics import  RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)

        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room)
            return Response(data=room_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room)
            return Response(data=serializer.data)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status.HTTP_403_FORBIDDEN)
            serializer = WriteRoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
#@api_view(["GET", "POST"])
#def rooms_view(request):
#    if request.method == "GET":
#        rooms = Room.objects.all()[:5]
#        serializer = ReadRoomSerializer(rooms, many=True)
#        return Response(serializer.data)
#        pass
#    elif request.method == "POST":
#        print(request.user)
#        if not request.user.is_authenticated:
#            return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#        serializer = WriteRoomSerializer(data=request.data)
#        if serializer.is_valid():
#            room = serializer.save(user=request.user)
#            room_serializer = ReadRoomSerializer(room).data
#            return Response(data=room_serializer, status=status.HTTP_200_OK)
#        else:
#            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#class SeeRoomView(RetrieveAPIView):
#    queryset = Room.objects.all()
#    serializer_class = ReadRoomSerializer
