import csv
import requests
import BeautifulSoup
from DBcrud import DBcrud

def GetEmbedHtml(TweetId):

    embedUrl = "https://api.twitter.com/1.1/statuses/oembed.json?id="+TweetId

    req = requests.get(embedUrl)
    jsonData = req.json() #load the json data returned from the request
    html = str(jsonData.get("html"))
    print(html)

    if html != None:

        htmltext = BeautifulSoup(html)
        [s.extract() for s in htmltext('script')]

        return htmltext
    else:
        return ""

def ExtractTweetsCsv(csvFile):

    tweets = []
    process = ""
    Users = ["tynetravel", "northyorktravel", "westyorkstravel", "teestravel", "floodAlerts", "riverlevelsuk", "southyorktravel"]

    with open(csvFile) as file:

        reader = csv.DictReader(file)
        leng = 0
        for row in reader:

            tweet = str.lower(row['tweet'])
            label = str.lower(row['Label'])
            TweetId = row["Id"]

            if ("flood" in tweet) and ("warning" not in tweet) and ("alert" not in tweet) and label not in Users:
                html = GetEmbedHtml(TweetId)
                tweets.append({"Time":row["TimeInterval"][2:25], "Lat":row["lat"], "Lng":row["lng"], "Label":row["Label"],
                                    "UserId":row["userid"], "TweetId":TweetId, "Tweet":tweet, "Html":html})
                leng = leng +1
                print "DONE:",leng
    return tweets

tweets = ExtractTweetsCsv("nodes.csv")
DB = DBcrud() #create a dbconnector/operator object
DB.addtweetdatabase(tweets)


