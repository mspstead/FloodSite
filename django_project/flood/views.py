from django.shortcuts import render
from .models import Photo

# Create your views here.

def index(request):
    photo_list = Photo.objects.all()
    context = {'photo_list':photo_list}
    return render(request,'flood/index.html', context)


def map(request):
    photo_list = Photo.objects.all()
    context = {'photo_list':photo_list}
    return render(request, 'flood/map.html', context)

def timeline(request):
    ordered_photo_list = Photo.objects.order_by("date_taken").distinct("locality")
    context = {'photo_list':ordered_photo_list}
    return render(request, 'flood/timeline.html', context)