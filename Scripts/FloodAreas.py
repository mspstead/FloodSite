import requests
import simplejson as json

def searchArea(lat,lng):
    """
    Search for any flood alerts in a particular area.
    :param lat:
    :param lng:
    :return:
    """

    searchUrl = "http://environment.data.gov.uk/flood-monitoring/id/floods?lat="+lat+"&long="+lng+"&dist=20"

    req = requests.get(searchUrl)
    jsonData = json.loads(req.text) #load the json data returned from the request

    floodAreaUrls = []
    for item in jsonData['items']:
        floodAreaUrls.append(item["@id"])

    return floodAreaUrls

def getFloodLocation(floodUrl):
    print(floodUrl)
    req = requests.get(floodUrl)
    jsonData = json.loads(req.text)
    latitude = jsonData["items"]["floodArea"]["lat"]
    longitude = jsonData["items"]["floodArea"]["long"]

floodurls = searchArea("51.7517","-1.2553")

getFloodLocation(floodurls[0])


