from django.http import HttpResponse
from django.shortcuts import render
from .models import Photo, RainLevel, Tweets
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

    ordered_photo_list = Photo.objects.order_by("date_taken") #order the photos based on the date_taken
    ordered_tweet_list = Tweets.objects.order_by("date_taken") #order the tweets based on date_taken
    combined_list = []

    for photo in ordered_photo_list:
        date = photo.date_taken
        combined_list.append([date,"photo",photo])

    for tweet in ordered_tweet_list:
        date = tweet.date_taken
        tweetHtml = tweet.html
        tweetHtml.replace('</script>', '"</scr"+"ipt>"')
        combined_list.append([date,"tweet",tweetHtml])

    combined_list.sort(key=lambda x: x[0])

    flood_events = getFloodEvents(ordered_photo_list)
    context = {'combined_list': combined_list, 'photo_list':ordered_photo_list, 'flood_events':flood_events, 'tweet_list':ordered_tweet_list}
    return render(request, 'flood/timeline.html', context)

def graph(request):

    ordered_photo_list = Photo.objects.order_by("date_taken") #order the photos based on the date_taken
    flood_events = getFloodEvents(ordered_photo_list)

    context = {'photo_list':ordered_photo_list, 'flood_events':flood_events}

    return render(request, 'flood/graph.html', context)

def upvote(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo.score += 1
    photo.save()
    return HttpResponse(status=204)

def downvote(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo.score -= 1
    photo.save()
    return HttpResponse(status=204)

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
