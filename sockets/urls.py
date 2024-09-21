from django.urls import path
from . import views

from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index, name='index'),
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
    
]