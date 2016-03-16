import requests
import simplejson as json
import time
import xml.etree.ElementTree as ET


AccessToken = "1964111288.2bcdedd.ff75c59254cc4511bb2fb36d0d8a53c3"
google_api_key = "AIzaSyBUpIx-7yc6wlReW5Wbd8gXAy7bvxHUFAQ"


def searchLocation(lat, lng):
    """
    Returns 20 most recent tweets based on location, all tweets are then searched for tags relating to flooding.
    :param lat:
    :param lng:
    :return:PhotoArray of all recent photos relating to flooding.
    """

    #searchUrl which is used to get the json data of all recent media in an area
    searchUrl = "https://api.instagram.com/v1/media/search?lat="+ lat +"&lng="+ lng +"&distance=5000" \
                + "&access_token=" + AccessToken
    #print(searchUrl)

    req = requests.get(searchUrl)

    jsonData = json.loads(req.text) #load the json data returned from the request

    for obj in jsonData['data']:
        for tag in obj['tags']:

            if tag == "flood": #cycle through the returned media and search for photos with tags=flood

                latitude = obj['location']['latitude'] #get the photos latitude
                longitude = obj['location']['longitude'] #get the longitude
                imageUrl = obj['images']['standard_resolution']['url'] #get the image url
                owner = obj['user']['username']
                date_taken = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(obj['created_time'])))
                title_text = obj['caption']['text']
                source = "instagram"
                locality = getLocality(str(latitude),str(longitude))
                print(str(latitude))

                print(latitude,longitude,imageUrl,owner,date_taken,title_text,locality)

            else:
                print("No results found")


def getLocality(lat,lon):

    """Uses Google's reverse geo-code API
    Takes latitude and longitude as its inputs
    returns a locality, e.g "Leeds"
    """

    locality_url = "https://maps.googleapis.com/maps/api/geocode/xml?latlng="+ lat + "," + lon +"&key=" + google_api_key
    r =requests.get(locality_url)
    root = ET.fromstring(r.text)

    for address in root[1].findall("address_component"): #cycle through all the address_components

        if(address.find("type").text == "postal_town"): #find the address_component with type=postal_town
            return address[0].text #get the first value of the address component (Long_name)

        else:
            return "Yorkshire"

#test location search
searchLocation("40.679373","17.932539")


