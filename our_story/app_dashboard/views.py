from django.http import HttpRequest
from django.shortcuts import render, redirect


def index(request):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')
    return render(request, 'app_dashboard/index.html')