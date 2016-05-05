#!/usr/bin python


import requests
import simplejson as json
import InstagramDailyScript
import time
from DB import DB

def searchArea(lat,lng,rad):
    """
    Search for any flood alerts in a radius area.
    :param lat:String
    :param lng:String
    :return:Array of data relating to flood warning areas, urls, description, severity, .
    """

    #search the api based on the lat,lng provided
    searchUrl = "http://environment.data.gov.uk/flood-monitoring/id/floods?lat="+lat+"&long="+lng+"&dist="+rad

    req = requests.get(searchUrl)

    #test json data used to check script is working properly
    #testJson = '{"@context" : "http://environment.data.gov.uk/flood-monitoring/meta/context.jsonld" , "meta" : { "publisher" : "Environment Agency" ,"licence" : "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" ,"documentation" : "http://environment.data.gov.uk/flood-monitoring/doc/reference" ,"version" : "0.6" ,"comment" : "Status: Beta service" ,"hasFormat" : [ "http://environment.data.gov.uk/flood-monitoring/id/floods.csv" ]},"items" : [ {"@id":"http://environment.data.gov.uk/flood-monitoring/id/floodAreas/053FWFPUWI06","description": "flood warning for leeds","severity": "Warning","severityLevel": "4","timeRaised": "01/01/2016 16:00:00"}, {"@id":"http://environment.data.gov.uk/flood-monitoring/id/floodAreas/061FWF23Goring", "description": "flood warning for Hebden Bride", "severity": "Alert", "severityLevel": "3", "timeRaised": "01/01/2016 15:00:00"} ]}'

    jsonData = json.loads(req.text) #load the json data returned from the request, or use testJson

    floodAreaInfo = [] #holds all the individual urls relating to any flooding in the search area
    for item in jsonData['items']:
        floodAreaInfo.append({'id':item["@id"], 'description':item["description"],
                              'severity':item["severity"], 'severitylevel':item["severityLevel"],
                              'time':item["timeRaised"]}) #add flood area dictionary to array
    #print floodAreaInfo

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
    latitude = jsonData["items"]["lat"] #get the latitude of the flood from the json data
    longitude = jsonData["items"]["long"] #get the longitude of the flood
    location.append(latitude)
    location.append(longitude)

    return location

def runInstagram(floodInfo):
    """
    run the instagram script on flood area lat and lng and add found data to DB
    :param floodInfo: floodArea url
    :return:
    """

    DBUpdate = DB()

    for flood in floodInfo: #cycle through all the flooded areas urls

        location = getFloodLocation(flood.get("id")) #get the flooded areas lat/lng
        print("location:",location)

        #search for any instagram posts relating to those locations and specified search term
        instaArray = InstagramDailyScript.searchLocation(str(location[0]),str(location[1]),"flood")

        print("Instagram Data:",instaArray)

        DBUpdate.addphotodatabase(instaArray)

def dailyExecute():
    floodInfo = searchArea("53.7996","-1.5491","20") #execute for 20km radius around leeds lat/lng

    if floodInfo != []: #check that there has been flood alerts

        for i in range(0,144): #cycle through 144 times as 144*600seconds = 24hours

            runInstagram(floodInfo) #run instagram script every 10minutes for 24hours, gets recent media
            print("sleeping 10minutes")
            time.sleep(600) #sleep for 10minutes
    else:
        print("No flood alerts")



