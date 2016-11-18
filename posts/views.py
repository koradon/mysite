from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def posts_home(request):

    return HttpResponse("<hi>Hello</h1>")
