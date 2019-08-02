from django.urls import path

from . import views


app_name = 'app_post'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('new/', views.new, name='new'),
    path('update/', views.update),
    path('heart/', views.heart),
    path('comment/', views.comment),
    path('remove/', views.remove),
]
