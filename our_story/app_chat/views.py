from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect

from .models import MessageBox


def index(request):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    message_list = list()
    for message_box in request.user.message_box_user.all():
        print(message_box.last_time)
        content = dict()
        content['user'] = message_box.friend
        content['unread'] = message_box.message.all().filter(to_user=request.user).aggregate(sum=Sum('unread'))['sum']
        content['unread'] = 0 if content['unread'] is None else content['unread']
        content['last_message'] = message_box.message.last().content
        message_list.append(content)
    return render(request, 'app_chat/index.html', {'message_list': message_list})


def message(request, friend, me):
    assert isinstance(request, HttpRequest)
    if not request.user.username in [friend, me]: raise Http404

    try:
        friend = User.objects.get(username=friend)
        query = Q(user=request.user) & Q(friend=User.objects.get(username=friend))
        message_box = MessageBox.objects.get(query)
    except:
        message_box = MessageBox.objects.create(user=request.user, friend=friend)
        MessageBox.objects.create(user=friend, friend=request.user)

    for message in reversed(message_box.message.all().filter(to_user=request.user).order_by('unread')):
        if message.unread == 0: break
        message.unread = 0
        message.save()
    return render(request, 'app_chat/message.html', {'friend': User.objects.get(username=friend).profile.get_name(), 'message_list': message_box.message.all()})
