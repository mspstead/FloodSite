import psycopg2
from django.conf import settings
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


    def addtweetdatabase(self, tweets):

        if len(tweets) > 1:

            try:
                conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
                curr = conn.cursor()

            except:
               print('ERROR:unable to connect')


            for tweet in tweets:

                tweetTime = tweet.get("Time")
                lat = tweet.get("Lat")
                lng = tweet.get("Lng")
                username = tweet.get("Label")
                userId = tweet.get("UserId")
                tweetId = tweet.get("TweetId")
                tweetMessage = tweet.get("Tweet")
                html = tweet.get("Html")
                curr.execute("INSERT INTO flood_tweets (date_taken,lat,lng,username,userid,tweetid,tweet,html) "
                               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(tweetTime,lat,lng,username,userId,tweetId,tweetMessage,html))

                print("ADDED: ", tweet)
            conn.commit()

        else:
            print("No tweets to add to DB")






