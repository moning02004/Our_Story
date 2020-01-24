from http import HTTPStatus

from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, JsonResponse, HttpResponse

from .models import Post, Heart, Comment, Image, Tag


def detail(request, pk):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    post = Post.objects.get(pk=pk)
    return render(request, 'app_post/detail.html', {'post': post})


def new(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        post = Post.objects.create(
            author=request.user,
            content=request.POST.get('content')
        )
        if request.POST.get('tag'):
            for tag in request.POST.get('tag').split(' '):
                try:
                    tag = Tag.objects.get(keyword=tag)
                except:
                    tag = Tag.objects.create(keyword=tag)
                post.tag.add(tag)

        if request.FILES.get('image'):
            for image in request.FILES.get('image'):
                Image.objects.create(post=post, file=image)

    return redirect('app_dashboard:index')


def edit(request, pk):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    post = Post.objects.get(pk=request.POST.get('pk'))
    if request.method == "POST":
        return redirect('app_post:detail', post.pk)
    return render(request, 'app_post/.html', {'post': post})


def update(request):
    assert isinstance(request, HttpRequest)
    post = request.POST.get('pk')
    return render(request, 'app_post/.html', {'post': post})


def heart(request):
    if request.is_ajax() and request.method == 'POST':
        post = Post.objects.get(pk=request.POST.get('pk'))
        if not request.user in [x.author for x in post.heart.all()]:
            heart = Heart.objects.create(author=request.user)
            post.heart.add(heart)
        else:
            post.heart.remove(post.heart.get(author=request.user))
            post.save()
        return HttpResponse(HTTPStatus.OK)
    return HttpResponse(HTTPStatus.BAD_REQUEST)


def comment(request):
    if request.is_ajax() and request.method == 'POST':
        post = Post.objects.get(pk=request.POST.get('pk'))
        comment = Comment.objects.create(post=post, author=request.user, content=request.POST.get('content'))
        response = {'content': comment.content, 'author': comment.author.profile.get_name(), 'created': comment.created.strftime('%Y-%m-%d %H:%M')}
        return JsonResponse(response)
    return HttpResponse(HTTPStatus.BAD_REQUEST)


def remove(request):
    if request.is_ajax() and request.method == 'POST':
        post = Post.objects.get(pk=request.POST.get('pk'))
        for x in post.image_set.all():
            x.delete()
        post.delete()
        return HttpResponse(HTTPStatus.OK)
    return HttpResponse(HTTPStatus.BAD_REQUEST)
