import requests
import simplejson as json
import InstagramDailyScript
import sched, time
import DBcrud

def searchArea(lat,lng):
    """
    Search for any flood alerts in a 20km radius area.
    :param lat:
    :param lng:
    :return:Array of Urls relating to flood warning areas.
    """

    #search the api based on the lat,lng provided
    searchUrl = "http://environment.data.gov.uk/flood-monitoring/id/floods?lat="+lat+"&long="+lng+"&dist=20"

    req = requests.get(searchUrl)
    #print(req.text)
    jsonData = json.loads(req.text) #load the json data returned from the request

    floodAreaUrls = [] #holds all the individual urls relating to any flooding in the search area
    for item in jsonData['items']:
        floodAreaUrls.append(item["@id"])

    return floodAreaUrls

def getFloodLocation(floodUrl):
    """
    get the specific latitude and longitude of any flood affected areas.
    :param floodUrl:
    :return:returns the latitude and longitude of a flooded area
    """
    location = [] #holds lat/lng
    print(floodUrl)
    req = requests.get(floodUrl)
    jsonData = json.loads(req.text)
    latitude = jsonData["items"]["floodArea"]["lat"] #get the latitude of the flood from the json data
    longitude = jsonData["items"]["floodArea"]["long"] #get the longitude of the flood
    location.append(latitude)
    location.append(longitude)

    return location

def runScripts(floodurls):

    #DBUpdate = DBcrud()

    for url in floodurls: #cycle through all the flooded areas urls

        location = getFloodLocation(url) #get the flooded areas lat/lng
        print(location)
        #search for any instagram posts relating to those locations and specified search term
        instaArray = InstagramDailyScript.searchLocation(str(location[0]),str(location[1],"flood"))
        print(instaArray)

        #DBUpdate.addtodatabase(instaArray)


floodurls = searchArea("53.7996","-1.5491") #execute for 20km radius around leeds lat/lng
runScripts(floodurls)
s = sched.scheduler(time.time, time.sleep)



