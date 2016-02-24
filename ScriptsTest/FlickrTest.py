import requests

url = "https://api.flickr.com/services/rest/?&method=flickr.photos.search&api_key=d5cb0ab00f8c5cfea4aac52760ba2615&tags=flood&has_geo=1&lat=53.7996&lon=-1.5491&radius=20&format=json"

r = requests.get(url)
print(r.text)
