from django.urls import path

from . import views


app_name = 'app_friend'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('add/', views.add),
    path('release/', views.release),
]