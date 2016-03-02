from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    return HttpResponse("Hello Michael <br/> <a href='map'>Map</a>")


def map(request):
    template = loader.get_template('/templates/map.html')
    return HttpResponse(template.render(request))