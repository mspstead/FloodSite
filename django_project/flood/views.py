from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Hello Michael <br/> <a href='/$/map/'>Map</a>")


def map(request):
    return HttpResponse("This is map page <a href='/$'>Index</a>")