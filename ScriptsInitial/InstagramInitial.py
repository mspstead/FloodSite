#import requests

access_token = '1964111288.2bcdedd.ff75c59254cc4511bb2fb36d0d8a53c3'

#url = "https://api.instagram.com/v1/media/search?lat=53.7996&lng=-1.5491&access_token="+ access_token

#req = requests.get(url)
#print(req.text)
from instagram.client import InstagramAPI

client_secret = "60d59c6cf6b24103ba6147669d05dcc3"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
popular_media = api.media_popular(count=20)
for media in popular_media:
    print media.images.url