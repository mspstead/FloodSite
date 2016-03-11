import psycopg2

class DBcrud:

    def addtodatabase(self, photoArray):

        if len(photoArray) > 1:

            try:
                conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
                curr = conn.cursor()

            except:
                print('ERROR:unable to connect')



            for photo in photoArray:
                owner = photo.get('Owner')
                title = photo.get('Title')
                date_taken = photo.get('date_taken')
                url = photo.get('Url')
                lat = photo.get('Lat')
                lng = photo.get('Lng')
                locality = photo.get('Locality')
                curr.execute("INSERT INTO flood_photo (owner, title_text, date_taken, url, lat, lng, locality) "
                              "VALUES (%s,%s,%s,%s,%s,%s,%s)",(owner,title,date_taken,url,lat,lng,locality))

            conn.commit()

        else:
            print("Nothing to add to DB.")




