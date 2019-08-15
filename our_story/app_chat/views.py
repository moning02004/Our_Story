from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect

from .models import MessageByUser


def index(request):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')
    return render(request, 'app_chat/index.html')


def message(request, friend, me):
    if not request.user.username in [friend, me]: raise Http404
    query = Q(participant=','.join(sorted([friend, me])))
    message_by_user = MessageByUser.objects.get(query)
    message_list = message_by_user.message.all()
    return render(request, 'app_chat/message.html', {'friend': User.objects.get(username=friend).profile.get_name(), 'message_list': message_list})
