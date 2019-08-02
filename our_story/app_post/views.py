from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, JsonResponse

from .models import Post, Heart, Comment


def detail(request, pk):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    post = Post.objects.get(pk=pk)
    return render(request, 'app_post/detail.html', {'post': post})


def new(request):
    if request.method == 'POST':
        Post.objects.create(
            author=request.user,
            content=request.POST.get('content')
        )
    return redirect('app_dashboard:index')


def edit(request, pk):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    post = request.POST.get('pk')
    return render(request, 'app_post/.html', {'post': post})


def update(request):
    post = request.POST.get('pk')
    return render(request, 'app_post/.html', {'post': post})


def heart(request):

    if request.is_ajax() and request.method == 'POST':
        post = Post.objects.get(pk=request.POST.get('pk'))
        print(post.heart.all())

        if not request.user in [x.author for x in post.heart.all()]:
            heart = Heart.objects.create(author=request.user)
            post.heart.add(heart)
        else:
            post.heart.remove(post.heart.get(author=request.user))
            post.save()
        return JsonResponse({'message': 'OK'})
    return JsonResponse({'message': 'NO'})


def comment(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            post = Post.objects.get(pk=request.POST.get('pk'))
            comment = Comment.objects.create(post=post, author=request.user, content=request.POST.get('content'))
            response = {'content': comment.content, 'author': comment.author.profile.get_name(), 'created': comment.created.strftime('%Y-%m-%d %H:%M')}
            return JsonResponse(response)
        return JsonResponse({'message': 'NO'})
    except:
        return JsonResponse({'message': 'NO'})


def remove(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            post = Post.objects.get(pk=request.POST.get('pk'))
            for x in post.image_set.all():
                x.delete()
            post.delete()
            return JsonResponse({'message': 'OK'})
        return JsonResponse({'message': 'NO'})
    except:
        return JsonResponse({'message': 'NO'})
