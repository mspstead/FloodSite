from django.http import HttpResponse
from django.shortcuts import render
from .models import Photo, Tweets, RiverLevel
from Scripts import FloodAreas

# Create your views here.

def index(request):
    floods = FloodAreas.searchArea("53.7996","-1.5491","20") #search within 20km of leeds for any flood warnings
    photos = Photo.objects.all()
    context = {'floods':floods} #return list of flood warnings send to webpage.
    return render(request,'flood/index.html', context)


def map(request):
    photo_list = Photo.objects.all() #get every photo object from database
    tweet_list = Tweets.objects.all() #get every tweet object from database
    context = {'photo_list':photo_list, 'tweet_list':tweet_list} #send to webpage
    return render(request, 'flood/map.html', context)

def timeline(request):

    ordered_photo_list = Photo.objects.order_by("date_taken") #order the photos based on the date_taken
    ordered_tweet_list = Tweets.objects.order_by("date_taken") #order the tweets based on date_taken
    combined_list = [] #holds both tweets and photos, so the timeline can display them in correct date order.

    for photo in ordered_photo_list: #cycle through photos and add to combined list
        date = photo.date_taken
        combined_list.append([date,"photo",photo])

    for tweet in ordered_tweet_list: #cycle through tweets and add to combined list
        date = tweet.date_taken
        combined_list.append([date,"tweet",tweet.html])

    combined_list.sort(key=lambda x: x[0]) #sort the list based on date_taken.

    flood_events = getFloodEvents(combined_list)

    context = {'combined_list': combined_list, 'flood_events': flood_events}
    return render(request, 'flood/timeline.html', context)

def upvote(request, photo_id):
    photo = Photo.objects.get(pk=photo_id) #get the specified photo based on its id
    photo.score += 1 #add 1 to the photos score
    photo.save() #save this new value
    return HttpResponse(status=204) #stay on the same webpage

def downvote(request, photo_id):
    photo = Photo.objects.get(pk=photo_id) #get the specified photo based on its id
    photo.score -= 1 #subtract 1 from its score
    photo.save()
    return HttpResponse(status=204) #stay on the same webpage

def getFloodEvents(list):
    """
    Method that returns a compiled list of flood_events.
    :param list: flood photos.
    :return: list of flood events.
    """

    ordered_list = list
    flood_events = [] #empty list to hold all of the flood events
    start_date = ordered_list[0][0].date() #Initialise start_date
    flood_event = [] #list to hold individual flood event dates

    for x in range(0, len(ordered_list)): #cycle through the list
        difference = (ordered_list[x][0].date() - start_date).days #calculate the difference between dates between photos
        if difference <= 1: #check the difference between dates is less than or equal to 1 day
            flood_event.append(ordered_list[x][0]) #if photos within 1 day of each other add to flood event
            start_date = ordered_list[x][0].date()
        else:
            flood_event.append(ordered_list[x-1][0])
            river_levels = RiverLevel.objects.filter(date_taken__gte=flood_event[0].date(), date_taken__lte=flood_event[-1].date())

            if len(flood_event) > 2:
                flood_events.append([flood_event[0],flood_event[-1],river_levels]) #add flood event to the flood_events list
            flood_event = [] #reset flood event to empty
        start_date = ordered_list[x][0].date() #set new start_date to the next photo date in list.
    return flood_events