import csv
import psycopg2
from datetime import datetime

def openCsv(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        rainLevels = []
        for row in reader:
            level = float(row['mm'])
            if level > 0 and level < 3:
                rainLevels.append([row['DateTime'],row['mm']])

    return rainLevels

def populateDB(rainLevels):
    if len(rainLevels) > 1:

        try:
            conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='localhost')
            curr = conn.cursor()
        except:
            print("Unable to connect")

        for rain in rainLevels:
            dateValue = datetime.strptime(rain[0],'%d/%m/%Y %H:%M').strftime('%Y/%m/%d %H:%M')
            mm = rain[1]
            ref = "Pottery Fields"
            curr.execute("INSERT INTO flood_rainlevel (date_taken,level,reference) "
                              "VALUES (%s,%s,%s)",(dateValue,mm,ref))
            print("ADDED:",rain)

        conn.commit()


levels = openCsv('RainGaugePtryF.csv')
populateDB(levels)
