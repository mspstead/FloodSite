import requests
import xml.etree.ElementTree as ET

api_key = "d5cb0ab00f8c5cfea4aac52760ba2615"
method = "flickr.photos.search"


def reqBuilder(tags, lat, lon, rad):
    """
    Build a search request based on tags (eg. flood), location(lat,lon) and radius(in km max=20), page default=1
    returns the flickr api data
    """
    requestArray = []

    # Create the url based on params given
    urlInit = "https://api.flickr.com/services/rest/?&method=" + method + "&api_key=" + api_key + "&tags=" + tags + \
           "&has_geo=1&lat=" + lat + "&lon=" + lon + "&radius=" + rad

    r = requests.get(urlInit)   # send the initial request
    requestArray.append(r)  # add the first request to the array

    tree = ET.fromstring(r.content) #get the content of first element

    number_of_pages = tree[0].get('pages') #get the number of pages, 250 results per page.

    if number_of_pages > 1:
        for num in range(1,int(number_of_pages)):    #cycle through the pages
            url = urlInit + "&page=" + str(num) #add the page to the initial url string
            r = requests.get(url)   #perform the get request for the url
            requestArray.append(r)  #add the request to the array

    return requestArray


def xmlParser(requestArray):

    photos = []  # array to hold the individual photo dictionary entries.
    for request in requestArray:
        tree = ET.fromstring(request.content) #get the xml content
        for photo in tree[0]: #extract the photos
            photos.append(photo.attrib)
    return photos


def photoUrlBuilder(photo):
    Id = photo.get('id')
    Server = photo.get('server')
    FarmId = photo.get('farm')
    Secret = photo.get('secret')

    photoUrl = "https://farm" + FarmId + ".staticflickr.com/" + Server + "/" + Id + "_" + Secret + ".jpg"

    return photoUrl




r = reqBuilder("flood", "53.7996", "-1.5491", "20")
photos = xmlParser(r)
print(len(photos))
for photo in photos:
    print(photo.get("title") ,photoUrlBuilder(photo))
