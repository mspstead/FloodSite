from django.http import HttpResponse
from django.shortcuts import render
from .models import Photo

# Create your views here.

def index(request):
    photo_list = Photo.objects.all()
    context = {'photo_list':photo_list}
    return(request,'flood/index.html', context)


def map(request):
    photo_list = Photo.objects.all()
    context = {'photo_list':photo_list}
    return render(request, 'flood/map.html')
