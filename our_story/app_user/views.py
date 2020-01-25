import re
from http import HTTPStatus

from django.contrib import auth
from django.http import HttpResponse, Http404, HttpRequest
from django.shortcuts import render, redirect
from .models import User


def login(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return render(request, 'app_dashboard/index.html')
    message = 'Nice To Meet You :)'

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.get(username=username)
            if user.check_password(password):
                auth.login(request, user)
                return redirect('app_dashboard:index')
        except:
            pass
        message = 'Check your username or password'
    return render(request, 'app_user/login.html', {'message': message})


def register(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return render(request, 'app_dashboard/index.html')

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        name = request.POST.get('name').strip()
        tel = request.POST.get('tel').strip()
        email = request.POST.get('email').strip()

        User.objects.create_user(
            username=username,
            password=password,
            name=name,
            tel=tel,
            email=email
        )
        return redirect('app_user:login')
    return redirect('app_main:index')


def profile(request, username):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')
    return render(request, 'app_user/profile.html', {'person': User.objects.get(username=username)})


def status(request):
    if request.is_ajax() and request.method == 'POST':
        request.user.status = request.POST.get('status')
        request.user.save()
        return HttpResponse(request.user.status, status=HTTPStatus.OK)
    raise Http404


def check_username(request):
    if request.is_ajax() and request.method == 'POST':
        username = request.POST.get('username')
        try:
            User.objects.all().get(username=username)
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except:
            return HttpResponse(status=HTTPStatus.OK)
    raise Http404


def logout(request):
    if request.is_ajax() and request.method == 'POST':
        auth.logout(request)
        return redirect('app_main:index')
    raise Http404


def edit(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        user = request.user
        print(request.FILES.get('profile-image'))
        user.avatar = request.FILES.get('profile-image') if request.FILES.get('profile-image') else user.avatar
        user.name = request.POST.get('name')
        user.address = request.POST.get('address')
        user.birth = request.POST.get('birth')
        user.gender = request.POST.get('gender')
        if check_password(request):
            user.set_password(request.POST.get('password'))
        user.save()
        return redirect('app_user:profile', request.user.username)
    return render(request, 'app_user/edit.html')


def check_password(request):
    password = request.POST.get('password')
    regex = re.compile('(?=.*[0-9])(?=.*[a-z]){8}')
    return regex.search(password) is not None