from http import HTTPStatus

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from app_user.models import User

from .models import MaybeKnow


def index(request):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    user = User.objects.prefetch_related('friend').get(username=request.user.username)
    people = user.maybe.all()
    return render(request, 'app_friend/index.html', {'people': people})


def add(request):
    if request.is_ajax() and request.method == 'POST':
        friend = User.objects.get(username=request.POST.get('username'))
        request.user.friend.add(friend)
        if not MaybeKnow.objects.filter(user=request.user, someone=friend).exists():
            MaybeKnow.objects.create(user=request.user, someone=friend)
        return HttpResponse(status=HTTPStatus.OK)
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)


def release(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            friend = User.objects.get(username=request.POST.get('username'))
            request.user.friend.remove(friend)
            return HttpResponse(status=HTTPStatus.OK)
        except:
            pass
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)


def search(request):
    keyword = request.GET.get('keyword')
    people = User.objects.filter(name=keyword).exclude(username=request.user.username) if User.objects.filter(name=keyword).exists() else []
    return render(request, 'app_friend/search.html', {'people': people})