import os

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404, HttpRequest
from django.shortcuts import render, redirect

from .models import Profile, Address


def login(request):
    if request.user.is_authenticated:
        return render(request, 'app_dashboard/index.html')
    message = 'Nice To Meet You : )'
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username)
            if user.check_password(password):
                auth.login(request, user)
                return redirect('app_dashboard:index')
        except:
            message = 'Check your username or password'
        else:
            message = 'Check your username or password'
    return render(request, 'app_user/login.html', {'message': message})


def register(request):
    if request.user.is_authenticated:
        return render(request, 'app_dashboard/index.html')
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        fname = request.POST.get('fname').strip()
        lname = request.POST.get('lname').strip()
        birth = request.POST.get('birth').strip()
        sex = request.POST.get('sex').strip()
        address = request.POST.get('address').strip()
        address_keywords = request.POST.get('address').strip().split(' ')

        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
        profile = Profile.objects.create(user=user, birth=birth, sex=sex, address=address)

        for x in address_keywords:
            if x == '': continue
            xx = Address.objects.create(keyword=x) if not x in [y.keyword for y in Address.objects.all()] else Address.objects.get(keyword=x)
            profile.address_keywords.add(xx)
        return redirect('app_user:login')
    return redirect('app_main:index')


def profile(request, username):
    if not request.user.is_authenticated:
        return redirect('app_main:index')
    return render(request, 'app_user/profile.html', {'user_': User.objects.get(username=username)})


def edit(request):
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    if request.method == 'POST':
        password = request.POST.get('password')
        fname = request.POST.get('fname').strip()
        lname = request.POST.get('lname').strip()
        birth = request.POST.get('birth').strip()
        sex = request.POST.get('sex').strip()
        address = request.POST.get('address').strip()
        address_keywords = request.POST.get('address').strip().split(' ')

        user = request.user
        user.first_name = fname
        user.last_name = lname
        user.save()

        print(request.FILES.get('profile-picture'))
        user.profile.picture.delete() if user.profile.picture else None
        user.profile.picture = request.FILES.get('profile-picture')
        user.profile.birth = birth
        user.profile.sex = sex
        user.profile.address = address
        user.profile.address_keywords.remove()
        user.profile.save()

        for x in address_keywords:
            if x == '': continue
            xx = Address.objects.create(keyword=x) if not x in [y.keyword for y in
                                                                Address.objects.all()] else Address.objects.get(
                keyword=x)
            user.profile.address_keywords.add(xx)
        return redirect('app_user:profile', request.user.username)
    return render(request, 'app_user/edit.html')


def check_username(request):
    if request.is_ajax() and request.method == 'POST':
        username = request.POST.get('username')
        message = 'OK' if not User.objects.all().filter(username=username).exists() and username != 'admin' else 'NO'
        return JsonResponse({'message': message})
    raise Http404


def logout(request):
    if request.is_ajax() and request.method == 'POST':
        auth.logout(request)
        return redirect('app_main:index')
    raise Http404
