'''Notes:
    Remove spaces from first line so csv.DictReader doesn't use them as part of the field names
    Delete last line, as it is only a repeat of the first line, this is how Moves > export > Excel writes the file.'''
import csv
charlist = []
with open('/home/mac/Shows/Fiddler/Fiddler_katie.csv', newline='') as f:
    cuereader = csv.DictReader(f)
    for row in cuereader:
        # print(row)
        print('{0}'.format(row['OnStage']))
        onstagefield = row['OnStage'].replace(' ','').replace('()','').split(',')
        # create a list of characters from the OnStage field
        for char in onstagefield:
            if char != '':
                if char not in charlist:
                    charlist.append(char)
    charlist.sort(reverse=True)
    print(charlist)
    charlistfile = open('/home/mac/Shows/Fiddler/FiddlerCharList.txt', 'w')
    for char in charlist:
        charlistfile.write('{0}\r'.format(char))
    charlistfile.close()
