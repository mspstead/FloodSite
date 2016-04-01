from django.shortcuts import render
from .models import Photo
import datetime

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
    ordered_photo_list = Photo.objects.order_by("date_taken")
    flood_events = []
    start_date = ordered_photo_list[0].date_taken
    for x in range(1, len(ordered_photo_list)):
        flood_event = []
        difference = (ordered_photo_list[x].date_taken - start_date).days
        print(difference)
        if difference < 7:
            flood_event.append(ordered_photo_list[x])
        else:
            flood_events.append(flood_event)
        start_date = ordered_photo_list[x]
    context = {'photo_list':ordered_photo_list, 'flood_events':flood_events}
    return render(request, 'flood/timeline.html', context)

def graph(request):
    return render(request, 'flood/graph.html')