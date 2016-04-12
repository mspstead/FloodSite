import requests
import simplejson as json
import InstagramDailyScript
import time
import DBcrud

def searchArea(lat,lng):
    """
    Search for any flood alerts in a 20km radius area.
    :param lat:
    :param lng:
    :return:Array of data relating to flood warning areas, urls, description, severity, .
    """

    #search the api based on the lat,lng provided
    searchUrl = "http://environment.data.gov.uk/flood-monitoring/id/floods?lat="+lat+"&long="+lng+"&dist=20"

    req = requests.get(searchUrl)
    #print(req.text)
    jsonData = json.loads(req.text) #load the json data returned from the request

    floodAreaInfo = [] #holds all the individual urls relating to any flooding in the search area
    for item in jsonData['items']:
        floodAreaInfo.append({'id':item["@id"], 'description':item["description"],
                              'severity':item["severity"], 'severitylevel':item["severityLevel"],
                              'time':item["timeRaised"]})

    return floodAreaInfo

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

def runInstagram(floodInfo):

    #DBUpdate = DBcrud()

    for flood in floodInfo: #cycle through all the flooded areas urls

        location = getFloodLocation(flood.get("id")) #get the flooded areas lat/lng
        print(location)
        #search for any instagram posts relating to those locations and specified search term
        instaArray = InstagramDailyScript.searchLocation(str(location[0]),str(location[1]),"flood")
        print(instaArray)

        #DBUpdate.addphotodatabase(instaArray)


floodInfo = searchArea("53.7996","-1.5491") #execute for 20km radius around leeds lat/lng

if floodInfo != []: #check that there has been flood alerts

    for i in range(0,144): #cycle through 144 times as 144*600seconds = 24hours

        runInstagram(floodInfo) #run instagram script every 10minutes for 24hours, gets recent media
        time.sleep(600) #sleep for 10minutes
else:
    print("No flooding")



