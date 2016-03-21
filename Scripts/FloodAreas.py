import requests
import simplejson as json
import InstagramDailyScript
import sched, time

def searchArea(lat,lng):
    """
    Search for any flood alerts in a 20km radius area.
    :param lat:
    :param lng:
    :return:Array of Urls relating to flood warning areas.
    """

    searchUrl = "http://environment.data.gov.uk/flood-monitoring/id/floods?lat="+lat+"&long="+lng+"&dist=20"

    req = requests.get(searchUrl)
    #print(req.text)
    jsonData = json.loads(req.text) #load the json data returned from the request

    floodAreaUrls = []
    for item in jsonData['items']:
        floodAreaUrls.append(item["@id"])

    return floodAreaUrls

def getFloodLocation(floodUrl):
    """
    get the specific latitude and longitude of any flood affected areas.
    :param floodUrl:
    :return:returns the latitude and longitude of a flooded area
    """
    location = []
    #print(floodUrl)
    req = requests.get(floodUrl)
    jsonData = json.loads(req.text)
    latitude = jsonData["items"]["floodArea"]["lat"]
    longitude = jsonData["items"]["floodArea"]["long"]
    location.append(latitude)
    location.append(longitude)

    return location

def runInstaScript(floodurls):

    for url in floodurls:
        location = getFloodLocation(url)
        print(location)
        InstagramDailyScript.searchLocation(str(location[0]),str(location[1]))

floodurls = searchArea("51.8699","-1.1208")
s = sched.scheduler(time.time, time.sleep)



