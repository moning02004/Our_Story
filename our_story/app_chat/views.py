from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect

from .models import MessageBox



def index(request):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')
    return render(request, 'app_chat/index.html')


def message(request, friend, me):
    if not request.user.username in [friend, me]: raise Http404
    query = Q(user=request.user) & Q(friend=User.objects.get(username=friend))
    messagebox = MessageBox.objects.get(query)
    message_list = messagebox.message.all()
    for x in message_list:
        if x.to_user == request.user:
            x.unread = 0
            x.save()
    return render(request, 'app_chat/message.html', {'friend': User.objects.get(username=friend).profile.get_name(), 'message_list': message_list})
