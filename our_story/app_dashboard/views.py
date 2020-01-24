from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect

from app_post.models import Post


def index(request):
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return redirect('app_main:index')

    query = Q(author=request.user)
    for x in request.user.friend.all():
        query.add(Q(author=x), query.OR)
    post_list = Post.objects.filter(query).order_by('created')
    return render(request, 'app_dashboard/index.html', {'post_list': reversed(post_list)})