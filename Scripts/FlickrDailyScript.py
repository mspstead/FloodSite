
import requests
import xml.etree.ElementTree as ET
import datetime
from DB import DB



"""
This is the script that will be run daily to extract any flooding photos that have been uploaded
on the previous day, so the database can stay up to date with the most recent flickr photos.
"""

api_key = "d5cb0ab00f8c5cfea4aac52760ba2615"
google_api_key = "AIzaSyBUpIx-7yc6wlReW5Wbd8gXAy7bvxHUFAQ"
search_method = "flickr.photos.search"
location_method = "flickr.photos.geo.getLocation"
date_method="flickr.photos.getInfo"

def reqBuilder(tags, lat, lon, rad):
    """
    Build a search request based on tags (eg. flood), location(lat,lon) and radius(in km max=20), min date uploaded,
    page default=1
    returns the flickr api data
    """
    requestArray = [] #holds all the return requests, there may be multiple pages = multiple requests.

    min_upload_date = datetime.datetime.today() - datetime.timedelta(days=1)
    print(min_upload_date)

    #Create the url based on params given, and include minimum date of yesterdays date.
    urlInit = "https://api.flickr.com/services/rest/?&method=" + search_method + "&api_key=" + api_key + \
              "&tags=" + tags + "&has_geo=1&lat=" + lat + "&lon=" + lon + "&radius=" + rad + \
              "&min_upload_date=" + min_upload_date.strftime("%y-%m-%d")

    r = requests.get(urlInit)   # send the initial request
    requestArray.append(r)  # add the first request to the array

    tree = ET.fromstring(r.content) #get the content of first element

    number_of_pages = tree[0].get('pages') #get the number of pages, 250 results per page.

    if number_of_pages > 1:
        for num in range(1,int(number_of_pages)):    #cycle through the pages
            url = urlInit + "&page=" + str(num+1) #add the page to the initial url string
            r = requests.get(url)   #perform the get request for the url
            requestArray.append(r)  #add the request to the array

    return requestArray


def xmlParser(requestArray):
    """
    Function to parse the xml from each request
    """

    photos = []  # array to hold the individual photo dictionary entries.
    for request in requestArray:
        tree = ET.fromstring(request.content) #get the xml content
        for photo in tree[0]: #extract the photos
            photos.append(photo.attrib) #add to the photos array
    return photos


def photoUrlBuilder(photo):
    """
    Function to construct and return the url string for a particular photo.
    """

    Id = photo.get('id') #get photo id
    Server = photo.get('server') #get photo server id
    FarmId = photo.get('farm') #get photo farm id
    Secret = photo.get('secret') #get photo secret code

    photoUrl = "https://farm" + FarmId + ".staticflickr.com/" + Server + "/" + Id + "_" + Secret + ".jpg" #compile url

    return photoUrl


def getLocation(Id):
    """
    Function to get and return the latitude and longitude of a particular photo.
    """

    LocationUrl = "https://api.flickr.com/services/rest/?&method=" + location_method + \
                  "&api_key=" +api_key + "&photo_id=" + Id #compile location api request based on photo's Id

    r = requests.get(LocationUrl) #perform get request for api
    root = ET.fromstring(r.content) #get the element tree root

    for child in root[0]: #get each individual xml element and extract relevant data
        lat = child.get("latitude")
        lon = child.get("longitude")

    locationArray = [lat, lon] #put latitude and longitude into an array
    return locationArray

def dateTaken(Id):
    """
    Function to get and return the date a particular photo was taken.
    """

    DateUrl = "https://api.flickr.com/services/rest/?&method=" + date_method + \
                  "&api_key=" +api_key + "&photo_id=" + Id #compile url for the date taken api request

    r = requests.get(DateUrl) #send the request
    root = ET.fromstring(r.content) #element tree root
    date_taken = root[0].find("dates").get("taken") # find the dates element and extract date/time it was taken

    return date_taken

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


def photoBuilder(photoArray):

    """
    Function to construct a photo dictionary which has all the important details of a photo added to a dictionary,
    the dictionary entry is then added to an array which is returned and can be used to add the photos to a DB.
    """

    photosDB = [] #An Array which will store all of the photo dictionarys
    #f = open('PhotoData.txt', 'w')
    #count = len(photoArray)

    for photo in photoArray: #cycle through all of the photos and extract the data to be stored

        id = photo.get('id')
        owner = photo.get('owner')
        title = photo.get('title')
        date_taken = dateTaken(id)
        url = photoUrlBuilder(photo)
        loc = getLocation(id)
        locality = getLocality(loc[0],loc[1])
        source = "Flickr"
        score = 0 #set photo's score to default value of 0

        #compile the dictionary
        photoDict = {"Id": id, "Owner":owner, "Title":title, "Url": url, "Lat":loc[0], "Lng":loc[1],
                     "Locality":locality, "Date_taken":date_taken, "Source":source, "Score":score}

        #print(photoDict)
        photosDB.append(photoDict) #add the current photo dictionary to the array

    return photosDB

r = reqBuilder("flood", "53.7996", "-1.5491", "20") #photos request being asked for
photos = xmlParser(r) #parse the requests
print(len(photos))
DBupdate = DB() #create a dbconnector/operator object
photoArray = (photoBuilder(photos)) #get the array of all the photos
DBupdate.addphotodatabase(photoArray) #add the photos to the database using method from DBcrud
