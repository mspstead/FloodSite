#Makes use of the python-instagram wrapper.

from instagram.client import InstagramAPI

access_token = '1964111288.2bcdedd.ff75c59254cc4511bb2fb36d0d8a53c3'
client_id = '2bcdedda8d4d44c6b32af10b083098ee'
client_secret = '60d59c6cf6b24103ba6147669d05dcc3'

api = InstagramAPI(access_token=access_token, client_id=client_id, client_secret=client_secret)

popular_media = api.media_popular(count=20)
for media in popular_media:
    print media.images.url
