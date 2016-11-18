from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post_create(request):
    return HttpResponse("create")


def post_detail(request):
    return HttpResponse("detail")


def post_list(request):
    return HttpResponse("list")


def post_update(request):
    return HttpResponse("update")


def post_delete(request):
    return HttpResponse("delete")
