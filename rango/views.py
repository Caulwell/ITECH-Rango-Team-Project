from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Rango says hey there partner! \r <a href='/rango/about/'>About</a>")

def about(request):
    return HttpResponse("Rango says here is the about page. \r <a href='/rango/'>Index</a>")