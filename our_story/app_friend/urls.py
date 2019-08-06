from django.urls import path

from . import views


app_name = 'app_friend'
urlpatterns = [
    path('', views.recommend, name='recommend'),
    path('add/', views.add),
    path('release/', views.release),
]