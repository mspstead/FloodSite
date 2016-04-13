import psycopg2

#First Initial database connection script to get the photo data from the text file and add to database.

try:
    conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
except:
    print("Unable to connect")

curr = conn.cursor()

data = open('PhotoData.txt', 'r')

for line in data:
    content = line.split(",")
    owner = content[0]
    title = content[1]
    date_taken = content[2]
    url = content[3]
    lat = content[4]
    lng = content[5]
    locality = content[6]

    curr.execute("INSERT INTO flood_photo (owner, title_text, date_taken, url, lat, lng, locality) VALUES (%s,%s,%s,%s,%s,%s,%s)", (owner,title,date_taken,url,lat,lng,locality))

conn.commit()
