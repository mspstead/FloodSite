import requests
import csv
from datetime import date, timedelta
from time import strftime
from DBcrud import DBcrud

base_url = "http://environment.data.gov.uk/flood-monitoring/archive/readings-"

leeds = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1707-level-stage-i-15_min-m"
kirkstall = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1708-level-stage-i-15_min-m"
castleford = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1703-level-stage-i-15_min-m"
tadcaster = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1304-level-stage-i-15_min-m"
mytholmroyd = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1204-level-stage-i-15_min-m"

def DownloadRiverData(start_date, end_date):

    delta = end_date - start_date

    river_file = open('YorkshireRiverLevels.txt', 'w')
    levels = []
    for x in range(delta.days +1):

        datecsv =  start_date + timedelta(days=x)
        requrl = base_url + datecsv.strftime("%Y-%m-%d") + ".csv"
        #print(requrl)
        request =  requests.get(requrl)

        csv_data = request.iter_lines()
        reader = csv.DictReader(csv_data)

        for row in reader:

            river_level = {}

            measure = row['measure']
            date = row['dateTime']
            value = row['value']

            if measure == leeds:
                river_level = {"measure":"Leeds", "datetime":date, "level":value, "lat":"53.794197", "lng":"-1.535433"}
                levels.append(river_level)

            elif measure == kirkstall:
                river_level = {"measure":"Kirkstall", "datetime":date, "level":value, "lat":"53.819613", "lng":"-1.605025"}
                levels.append(river_level)

            elif measure == castleford:
                river_level = {"measure":"castleford", "datetime":date, "level":value, "lat":"53.731002", "lng":"-1.358177"}
                levels.append(river_level)

            elif measure == tadcaster:
                river_level = {"measure":"tadcaster", "datetime":date, "level":value, "lat":"53.677173", "lng":"-1.491306"}
                levels.append(river_level)

            elif measure == mytholmroyd:
                river_level = {"measure":"mytholmroyd", "datetime":date, "level":value, "lat":"53.73128", "lng":"-1.983282"}
                levels.append(river_level)

            #if river_level != {}:

                #river_file.write(river_level.get("measure")+","+river_level.get("datetime")+","+
                    #river_level.get("level")+","+river_level.get("lat")+","+river_level.get("lng")+"\n")

            #print (river_level)
        print(datecsv.strftime("%Y-%m-%d")+", completed.")
    DB = DBcrud()
    DB.addRiverLevel(levels)
    #river_file.close()

def readFromFile(fileName):

    data = open(fileName, 'r')
    levels = []
    for line in data:
        content = line.split(",")
        place = content[0]
        date_taken = content[1]
        level = content[2]
        lat = content[3]
        lng = content[4]
        river_level = {"measure":place, "datetime":date_taken, "level":level, "lat":lat, "lng":lng}
        levels.append(river_level)
    DB = DBcrud()
    DB.addRiverLevel(levels)

strt_date = date(2015,01,15)
ed_date = date(2016,01,10)

#DownloadRiverData(strt_date,ed_date)
readFromFile("YorkshireRiverLevels.txt")


