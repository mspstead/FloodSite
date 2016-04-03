import csv
import psycopg2

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
            conn = psycopg2.connect(database='django', user='django', password='AgZP7U56Mw', host='http://46.101.11.228')
            curr = conn.cursor()
        except:
            print("Unable to connect")

        for rain in rainLevels:
            dateValue = rain[0]
            mm = rain[1]
            ref = "Pottery Fields"
            curr.execute("INSERT INTO flood_rainlevel (date_taken,level,reference) "
                              "VALUES (%s,%s,%s)",(dateValue,mm,ref))
            print("ADDED:",rain)


levels = openCsv('RainGaugePtryF.csv')
populateDB(levels)