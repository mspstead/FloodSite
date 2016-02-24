import requests

api_key = "d5cb0ab00f8c5cfea4aac52760ba2615"
method = "flickr.photos.search"


def reqBuilder(tags, lat, lon, rad):
    """
    Build a search request based on tags and location and radius
    """
    url1 = "https://api.flickr.com/services/rest/?&method=" + method + "&api_key=" + api_key + "&tags=" + tags +\
           "&has_geo=1&lat=" + lat + "&lon=" + lon + "&radius=" + rad
    r = requests.get(url1)
    print(r.text)


reqBuilder("flood", "53.7996", "-1.5491", "20")
