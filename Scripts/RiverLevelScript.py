import requests
import csv
from datetime import date, timedelta
from time import strftime
from DB import DB

base_url = "http://environment.data.gov.uk/flood-monitoring/archive/readings-" #Url used to request csv files

#Measure Urls used to filter the data
leeds = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1707-level-stage-i-15_min-m"
kirkstall = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1708-level-stage-i-15_min-m"
castleford = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1703-level-stage-i-15_min-m"
tadcaster = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1304-level-stage-i-15_min-m"
mytholmroyd = "http://environment.data.gov.uk/flood-monitoring/id/measures/L1204-level-stage-i-15_min-m"

def DownloadRiverData(start_date, end_date):
    """
    Gets river level data for particular days and locations, adds to database and/or save to file
    :param start_date: date object, Y m d
    :param end_date: date object, Y m d
    :return:
    """

    delta = end_date - start_date #calculate the number of days between the dates

    river_file = open('YorkshireRiverLevels.txt', 'w') #text file which processed data will be saved to.
    levels = [] #empty array to hold river level dictionary objects

    for x in range(delta.days +1): #cycle through the days

        datecsv =  start_date + timedelta(days=x) #the date which is to be queried
        requrl = base_url + datecsv.strftime("%Y-%m-%d") + ".csv" #create the url used to request the csv file
        #print(requrl)
        request = requests.get(requrl) #request the file

        csv_data = request.iter_lines() #read the csv file
        reader = csv.DictReader(csv_data)

        for row in reader: #cycle through each line in the csv file

            river_level = {} #initialise river level dictionary

            measure = row['measure'] #get the measure URL, date and river level
            date = row['dateTime']
            value = row['value']

            if measure == leeds: #check if measure Url = leeds measure url and add relevant data to dictionary
                river_level = {"measure":"Leeds", "datetime":date, "level":value, "lat":"53.794197", "lng":"-1.535433"}
                levels.append(river_level) #add to array

            elif measure == kirkstall: #check if measure Url = kirkstall measure url and add relevant data to dictionary
                river_level = {"measure":"Kirkstall", "datetime":date, "level":value, "lat":"53.819613", "lng":"-1.605025"}
                levels.append(river_level)

            elif measure == castleford: #check if measure Url = castleford measure url and add relevant data to dictionary
                river_level = {"measure":"castleford", "datetime":date, "level":value, "lat":"53.731002", "lng":"-1.358177"}
                levels.append(river_level)

            elif measure == tadcaster: #check if measure Url = tadcaster measure url and add relevant data to dictionary
                river_level = {"measure":"tadcaster", "datetime":date, "level":value, "lat":"53.677173", "lng":"-1.491306"}
                levels.append(river_level)

            elif measure == mytholmroyd: #check if measure Url = mytholmroyd measure url and add relevant data to dictionary
                river_level = {"measure":"mytholmroyd", "datetime":date, "level":value, "lat":"53.73128", "lng":"-1.983282"}
                levels.append(river_level)

            if river_level != {}: #if the dictionary contains data write the data to the file

                river_file.write(river_level.get("measure")+","+river_level.get("datetime")+","+
                    river_level.get("level")+","+river_level.get("lat")+","+river_level.get("lng")+"\n")

            #print (river_level)
        print(datecsv.strftime("%Y-%m-%d")+", completed.") #output the completed day
    DBupdate = DB()
    DBupdate.addRiverLevel(levels) #add data to database using levels array
    river_file.close() #close the file

def readFromFile(fileName):
    """
    Saves river-level data from file to database
    :param fileName: file produced by DownloadRiverData()
    :return:
    """

    data = open(fileName, 'r') #open the file
    levels = [] #create an array to hold the river level dictionaries

    for line in data: #examine each line in file
        content = line.split(",") #seperate data by comma and get the relevant valyes
        place = content[0]
        date_taken = content[1]
        level = content[2]
        lat = content[3]
        lng = content[4]
        river_level = {"measure":place, "datetime":date_taken, "level":level, "lat":lat, "lng":lng} #save data to dictionary
        levels.append(river_level) #add to array
    DBupdate = DB()
    DBupdate.addRiverLevel(levels) #add data to database using levels array

strt_date = date(2015,11,14) #set the start date, earliest start date of 15/01/2015
ed_date = date(2016,01,10) #set the end date, max end date of  yesterdays date

#DownloadRiverData(strt_date,ed_date) # uncomment to execute either function
#readFromFile("YorkshireRiverLevels.txt")


