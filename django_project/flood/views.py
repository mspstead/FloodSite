from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("Hello Michael <br/> <a href='map'>Map</a>")


def map(request):
    return render(request, 'flood/map.html')
