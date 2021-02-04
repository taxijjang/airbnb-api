from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    #path("list/", views.ListRoomsView.as_view()),
    path("list/",views.RoomsView.as_view()),
    path("<int:pk>/", views.Room),
]
