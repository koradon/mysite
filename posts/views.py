from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")


def post_create(request):
    return HttpResponse("create")


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "title": "Detail",
        "objects_list": queryset,
    }
    return render(request, "index.html", context)


def post_update(request):
    return HttpResponse("update")


def post_delete(request):
    return HttpResponse("delete")
