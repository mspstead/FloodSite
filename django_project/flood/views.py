from django.shortcuts import render
from .models import Photo, RainLevel
import itertools as it
from datetime import datetime, timedelta

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
    flood_events = getFlood(ordered_photo_list)

    context = {'photo_list':ordered_photo_list, 'flood_events':flood_events}
    return render(request, 'flood/timeline.html', context)

def graph(request):

    ordered_photo_list = Photo.objects.order_by("date_taken") #order the photos based on the date_taken
    flood_events = getFloodEvents(ordered_photo_list)

    context = {'photo_list':ordered_photo_list, 'flood_events':flood_events}

    return render(request, 'flood/graph.html', context)

def getFloodEvents(list):
    ordered_list = list
    flood_events = [] #empty list to hold all of the flood events
    start_date = ordered_list[0].date_taken.date() #Initialise start_date
    flood_event = [] #list to hold individual flood event photo objects

    for x in range(0, len(ordered_list)): #cycle through the list
        difference = (ordered_list[x].date_taken.date() - start_date).days #calculate the difference between dates between photos
        if difference <= 1: #check the difference between dates is less than or equal to 1 day
            flood_event.append(ordered_list[x].date_taken) #if photos within 1 day of each other add to flood event
            start_date = ordered_list[x].date_taken.date()
        else:
            flood_event.append(ordered_list[x-1].date_taken)
            rain_levels = RainLevel.objects.filter(date_taken__gte=flood_event[0].date(), date_taken__lte=flood_event[-1].date())
            flood_events.append([flood_event[0],flood_event[-1],rain_levels]) #add flood event to the flood_events list
            flood_event = [] #reset flood event to empty
        start_date = ordered_list[x].date_taken.date() #set new start_date to the next photo date in list.
    return flood_events

def getFlood(list):
    # Remove duplicates, and sort the dates ascending
    sorted_dates = sorted(set(list))
    # Set initial first and last element as the current element
    first, last = sorted_dates[0].date_taken, sorted_dates[0].date_taken
    flood_events = []

    # Loop over the sorted list from the second value
    for d in sorted_dates[1:]:
        # Check if the current date is exactly one day later then the current
        # "last" date
        if d.date_taken - last != timedelta(days=1):
            rain_levels = RainLevel.objects.filter(date_taken__gte=d.date_taken.date(), date_taken__lte=last)
            flood_events.append([first, last, rain_levels])
            first, last = d.date_taken, d.date_taken
        else:
            last = d.date_taken

    # Handle last element
    rain_levels = RainLevel.objects.filter(date_taken__gte=d.date(), date_taken__lte=last.date())
    if first == last:
        flood_events.append(([first, last, rain_levels]))
    else:
        flood_events.append([first, last, rain_levels])

    return flood_events