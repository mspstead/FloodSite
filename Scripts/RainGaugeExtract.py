import csv

def openCsv(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        rainLevels = []
        largest =
        for row in reader:
            level = float(row['mm'])
            if level > 0 and level < 3:
                rainLevels.append([row['DateTime'],row['mm']])
        for rain in rainLevels:
            print(rain)
openCsv('RainGaugePtryF.csv')