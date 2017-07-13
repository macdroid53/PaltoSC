import csv
charlist = []
MixerMap = open('/home/mac/Shows/Fiddler/MixerMapx.xml', mode='w')
MixerMap.write('<?xml version="1.0" encoding="UTF-8"?>\n')
with open('/home/mac/Shows/Fiddler/FiddlerCharList_adjusted.csv', newline='') as f:
    cuereader = csv.DictReader(f)
    cuereader_list = list(cuereader)
    charcount = len(cuereader_list) - 1
    MixerMap.write('<mixermap charcount="{0}" auxcount="0">\n'.format(charcount))
    for i, row in enumerate(cuereader_list):
        MixerMap.write('\t<input mixerid="0" chan="{0}" actor="{1}" char="{2}"/>\n'.format(i+1, row['actor'], row['char']))
        print('mixerid="0" chan="{0}" actor="{1}" char="{2}"'.format(i, row['actor'], row['char']))
MixerMap.write('</mixermap>')
MixerMap.close()

