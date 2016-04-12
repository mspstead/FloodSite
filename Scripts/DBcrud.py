import psycopg2
from django.db import models
from django_project.flood.models import Photo, Tweets

class DBcrud:

    def addphotodatabase(self, photoArray):

        if len(photoArray) > 1:

            try:
                conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
                curr = conn.cursor()

            except:
                print('ERROR:unable to connect')



            for photo in photoArray:
                owner = photo.get('Owner')
                title = photo.get('Title')
                date_taken = photo.get('Date_taken')
                url = photo.get('Url')
                lat = photo.get('Lat')
                lng = photo.get('Lng')
                locality = photo.get('Locality')
                source = photo.get('Source')
                score = photo.get('Score')
                curr.execute("INSERT INTO flood_photo (owner, title_text, date_taken, url, lat, lng, locality, source, score) "
                              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(owner,title,date_taken,url,lat,lng,locality,source,score))
                print("ADDED: ", photo)

            conn.commit()

        else:
            print("Nothing to add to DB.")


    def addtweetdatabase(self, tweetList):

        if len(tweetList) > 1:

            for tweet in tweetList:
                tweetTime = tweet.get("Time")
                latitude = tweet.get("Lat")
                longitude = tweet.get("Lng")
                user = tweet.get("Label")
                userId = tweet.get("UserId")
                tweetId = tweet.get("TweetId")
                tweetMessage = tweet.get("Tweet")
                Html = tweet.get("Html")
                tweetObject = Tweets(date_taken=tweetTime, lat=latitude, lng= longitude, username=user,
                                     userid=userId, tweetid=tweetId, tweet=tweetMessage, html=Html)
                tweetObject.save()
                print("Added tweet to database")

        else:
            print("No tweet to add to db")






