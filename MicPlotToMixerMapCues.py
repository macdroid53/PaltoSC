import csv
charlist = []
with open('/home/mac/Shows/Fiddler/Fiddler-1_MP-2.csv', newline='') as f:
    cuereader = csv.DictReader(f)
    for row in cuereader:
        list = list(cuereader)
        print(row.keys())
        print(row)
        #print('{0}'.format(row['OnStage']))
