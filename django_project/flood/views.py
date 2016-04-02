from django.shortcuts import render
from .models import Photo
import itertools as it

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
    ordered_photo_list = Photo.objects.order_by("date_taken") #order the photos based on the date_taken
    flood_events = [] #empty list to hold all of the flood events
    start_date = ordered_photo_list[0].date_taken #Initialise start_date
    flood_event = [] #list to hold individual flood event photo objects
    for x in range(0, len(ordered_photo_list)): #cycle through the list
        difference = (ordered_photo_list[x].date_taken - start_date).days #calculate the difference between dates between photos
        if difference <= 7: #check the difference is less than or equal to 7 days
            flood_event.append(ordered_photo_list[x]) #if photos within 7 days of each other add to flood event
            #start_date = ordered_photo_list[x].date_taken #set new start_date to current photo date in list.

        else:
            flood_events.append(flood_event) #add flood event to the
            flood_event = [] #reset flood event to empty
            start_date = ordered_photo_list[x+1].date_taken #set new start_date to current photo date in list.
    context = {'photo_list':ordered_photo_list, 'flood_events':flood_events}
    return render(request, 'flood/timeline.html', context)

def graph(request):
    return render(request, 'flood/graph.html')