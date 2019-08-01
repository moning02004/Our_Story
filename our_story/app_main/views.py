from django.http import HttpRequest
from django.shortcuts import render, redirect


def index(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return redirect('app_dashboard:index')
    return render(request, 'app_user/register.html')