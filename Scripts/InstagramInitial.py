import twitter

api = twitter.Api(
 consumer_key='sNMOctZzqS16Z9COfJQc73KS5',
 consumer_secret='anyHcZjyf4NVgg16g6tvYU647J30nIVaiUuCb0qpIdzvhRPann',
 access_token_key='1454778379-9MxHIctdm8jPLqUKsEZPLo6To39W74VxoWnu6ZK',
 access_token_secret='6bKrwXPkhcpWP2fBGVq227U317IiNni8hxvrovf55QAIu'
 )

search = api.GetSearch(term="%23flood", geocode=("53.79", "-1.54", "20mi") ,until="2015-12-28")
for t in search:
 print t.user.screen_name + ' (' + t.created_at + ')'
 #Add the .encode to force encoding
 print t.text.encode('utf-8')

def searchTweets(start_date, end_date, query, lat, lng):

    searchUrl = "https://api.twitter.com/1.1/search/tweets.json?q="+query+"&until="+end_date
    query = "q=%23flood&geocode=53.79,-1.54,20mi&until=2015-12-30"


