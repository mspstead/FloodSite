import psycopg2

try:
    conn = psycopg2.connect(database='django', user='', password='', host='46.101.11.228', port='5432')
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

    query = ("INSERT INTO flood_table VALUES (%s)", (owner,title,date_taken,url,lat,lng,locality))
    curr.execute(query)
