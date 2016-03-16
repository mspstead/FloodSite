import requests
import simplejson as json
import InstagramDailyScript

def searchArea(lat,lng):
    """
    Search for any flood alerts in a 20km radius area.
    :param lat:
    :param lng:
    :return:
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
    :return:
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

floodurls = searchArea("53.7996","-1.5491")

for url in floodurls:
    location = getFloodLocation(url)
    InstagramDailyScript.searchLocation(str(location[0]),str(location[1]))


