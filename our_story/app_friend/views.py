from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from app_user.models import User


def recommend(request):
    rec_friend_list = []
    for x in request.user.profile.address_keywords.all():
        for profile in Address.objects.get(keyword=x.keyword).profile_set.all():
            rec_friend_list.append(profile) if profile not in rec_friend_list and profile != request.user.profile else None

    print(rec_friend_list)
    return render(request, 'app_friend/recommend.html', {'recommended_friend_list': rec_friend_list})


def add(request):
    if request.is_ajax() and request.method == 'POST':
        target = Profile.objects.get(user=User.objects.get(username=request.POST.get('username')))
        request.user.profile.friend.add(target) if target not in request.user.profile.friend.all() else None
        return JsonResponse({'message':'OK'})
    return JsonResponse({'message':'NO'})


def release(request):
    if request.is_ajax() and request.method == 'POST':
        target = Profile.objects.get(user=User.objects.get(username=request.POST.get('username')))
        request.user.profile.friend.remove(target) if target in request.user.profile.friend.all() else None
        return JsonResponse({'message':'OK'})
    return JsonResponse({'message': 'NO'})
