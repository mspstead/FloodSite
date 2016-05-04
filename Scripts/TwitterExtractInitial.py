import csv
import requests
import BeautifulSoup
from DB import DB

#Initial twitter script to extract relevant tweets from a csv file of tweets provided.

def GetEmbedHtml(TweetId):

    embedUrl = "https://api.twitter.com/1.1/statuses/oembed.json?id="+TweetId #send request for tweet embed info

    req = requests.get(embedUrl)

    jsonData = req.json() #load the json data returned from the request

    html = jsonData.get("html") #Get the tweets embed html, so tweet can be embedded on website

    if html != None: #check that tweet has embed html

        htmltext = BeautifulSoup.BeautifulSoup(html) #parse html using BeautifulSoup

        [s.extract() for s in htmltext('script')] #remove all javascript from the html embed code

        tweetHtml = str(htmltext).replace("\n", "") #remove all line breaks

        return str(tweetHtml)
    else:
        return ""

def ExtractTweetsCsv(csvFile):

    tweets = [] #Array to hold tweet dictionaries

    #These users in the data produce irrelevant flood alerts, typically every 15minutes
    Users = ["tynetravel", "northyorktravel", "westyorkstravel", "teestravel", "floodAlerts", "riverlevelsuk", "southyorktravel"]

    with open(csvFile) as file:

        reader = csv.DictReader(file) #open the csv file

        leng = 0 #used as a counter to see how many tweets are processed

        for row in reader:

            tweet = str.lower(row['tweet']) #get the tweet message in lower-case
            label = str.lower(row['Label']) #get the users name in lower-case
            TweetId = row["Id"] #get the tweets Id

            #Search for any term flood in tweet message, check warning is not in tweet message and check its not from specified users.
            if ("flood" in tweet) and ("warning" not in tweet) and ("alert" not in tweet) and label not in Users:

                html = GetEmbedHtml(TweetId) #get tweets embed html

                tweetDict = {"Time":row["TimeInterval"][2:25], "Lat":row["lat"], "Lng":row["lng"], "Label":row["Label"],
                                    "UserId":row["userid"], "TweetId":TweetId, "Tweet":tweet, "Html":html}

                tweets.append(tweetDict)

                leng = leng +1 #add one to process tweets

                print "DONE:",leng #output tweets number of tweets completed
                print "Tweet:",tweetDict
    return tweets

tweets = ExtractTweetsCsv("nodes.csv")
DBupdate = DB() #create a dbconnector/operator object
DBupdate.addtweetdatabase(tweets) #add tweets to database


