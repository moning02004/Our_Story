from django.urls import path

from . import views


app_name = 'app_user'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit),
    path('check_username/', views.check_username),
    path('logout/', views.logout, name='logout'),
]