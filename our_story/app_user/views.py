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
        username = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        birth = request.POST.get('birth').strip()
        sex = request.POST.get('sex')
        address = request.POST.get('address').strip().split(' ')

        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
        profile = Profile.objects.create(user=user, birth=birth, sex=sex)

        for x in address:
            if x == '': continue
            xx = Address.objects.create(keyword=x) if not x in [y.keyword for y in Address.objects.all()] else Address.objects.get(keyword=x)
            profile.address.add(xx)
        return redirect('app_user:login')
    return redirect('app_main:index')


def profile(request):
    return None


def edit(request):
    return None


def check_username(request):
    if request.is_ajax() and request.method == 'POST':
        message = 'OK' if not User.objects.all().filter(username=request.POST.get('username')).exists() else 'NO'
        return JsonResponse({'message': message})
    raise Http404


def logout(request):
    if request.is_ajax() and request.method == 'POST':
        auth.logout(request)
        return redirect('app_main:index')
    raise Http404
