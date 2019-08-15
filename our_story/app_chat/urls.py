from django.urls import path

from . import views


app_name = 'app_chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('message/<str:friend>/<str:me>/', views.message, name='message')
]