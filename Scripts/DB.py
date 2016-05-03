import psycopg2


class DB:

    def addphotodatabase(self, photoArray):
        """
        Method used to add photos to the database
        :param photoArray: Array of photo dictionarys
        :return:
        """

        if len(photoArray) > 1: #check that there is atleast 1 photo in the array.

            try:
                #try to connect to the database
                conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
                curr = conn.cursor()

            except:
                print('ERROR:unable to connect')



            for photo in photoArray: #cycle through the photos, extract the relevant data to be added to the database

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

            conn.commit() #Commit all the photos to the database

        else:
            print("Nothing to add to DB.")


    def addtweetdatabase(self, tweets):

        """
        Method to add tweets to the database.
        :param tweets: array of tweet dictionaries
        :return:
        """

        if len(tweets) > 1: #check atleast 1 tweet in array

            try:
                conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
                curr = conn.cursor()

            except:
               print('ERROR:unable to connect')


            for tweet in tweets: #cycle through the tweets and extract the relevant information and add to database

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

            conn.commit() #commit the added tweets to the databse

        else:
            print("No tweets to add to DB")


    def addRiverLevel(self, levels):

        if len(levels) > 1: #check atleast 1 tweet in array

            try:
                conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
                curr = conn.cursor()

            except:
               print('ERROR:unable to connect')


            for level in levels: #cycle through the tweets and extract the relevant information and add to database

                date_taken = level.get("datetime")
                place = level.get("measure")
                river_level = level.get("level")
                lat = level.get("lat")
                lng = level.get("lng")

                curr.execute("INSERT INTO flood_riverlevel (date_taken,place,river_level,lat,lng) "
                               "VALUES (%s,%s,%s,%s,%s)",(date_taken,place,river_level,lat,lng))

                print("ADDED: ", level)

            conn.commit()

        else:
            print("No river levels to add")
