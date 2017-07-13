import uuid
import csv
import re
try:
    from lxml import ET
except ImportError:
    import xml.etree.ElementTree as ET

def getmixermap(mapfile):
    mixermap = ET.parse(mapfile)
    charcount = int(mixermap.getroot().attrib['charcount'])

    chars = mixermap.findall('input')
    chardict = {}
    for char in chars:
        cnum = int(char.attrib['chan'])
        mxrid = int(char.attrib['mixerid'])
        char = char.attrib['char']
        chardict[char] = 'M{0:1}ch{1:02}'.format(mxrid, cnum)
    return chardict

def putcuefile(newdoc, cuedict, cuenum):

    cueele = ET.SubElement(newdoc, 'Cue', {'uuid':'{0}'.format(uuid.uuid4()), 'num' : '{0:003}'.format(cuenum)})

    for key in cuedict:
        print('key: {0}'.format(key))
        firstlevelel = ET.SubElement(cueele, key)
        if type(cuedict[key]) is not dict:
            print('**')
            print(cuedict[key])
            firstlevelel.text = cuedict[key]
        else:
            children = cuedict[key]
            for child in children:
                print('child: {0}, childval: {1}'.format(child, children[child]))
                secondlevel = ET.SubElement(firstlevelel, child)
                secondlevel.text = children[child]
                pass
    return newdoc


if __name__ == "__main__":
    mixermapdict = getmixermap('/home/mac/Shows/Fiddler/MixerMapx.xml')
    mutes = {}
    for chan in mixermapdict:
        print('Char: {0} Chan: {1}'.format(chan, mixermapdict[chan]))
        mutes[mixermapdict[chan]] = 0
    newdoc = ET.Element('show_control')
    with open('/home/mac/Shows/Fiddler/Fiddler_katie.csv', newline='') as f:
        cuereader = csv.DictReader(f)
        for cue_num, row in enumerate(cuereader):
            print('{0},{1},{2},{3}'.format(row['A'],row['S'],row['Page'],row['Id']))
            newcue = {}
            #newcue['cue'] = {'uuid' : '{0}'.format(uuid.uuid4()), 'num' : '{0:003}'.format(cue_num)}
            newcueelements = {}
            newcueelements['Id'] = row['Id']
            newcueelements['Act'] = row['A']
            newcueelements['Scene'] = row['S']
            newcueelements['Page'] = row['Page']
            newcueelements['Title'] = row['Title']
            newcueelements['CueCall'] = row['Cue']
            newcueelements['CueType'] = 'Mixer'
            newcueelements['Note1'] = ''
            newcueelements['Note2'] = ''
            newcueelements['Note3'] = ''
            # print(row)
            print('Entrances: {0}'.format(row['Entrances']))
            entrances = row['Entrances'].split(',')
            for ent in entrances:
                try:
                    ent_char, ent_actor = ent.split('(')
                except ValueError:
                    ent_char = ent
                char = ent_char.strip()
                if char not in mixermapdict:
                    print('{0} not found!'.format(ent))
                if char != '' and char in mixermapdict:
                    mixerchan = mixermapdict[char.replace(' ','')]
                    mutes[mixerchan] = 1
            print('Exits: {0}'.format(row['Exits']))
            exits = row['Exits'].split(',')
            for xit in exits:
                try:
                    xit_char, xit_actor = xit.split('(')
                except ValueError:
                    xit_char = ent
                char = xit_char.strip()
                if char not in mixermapdict:
                    print('{0} not found!'.format(xit))
                if char != '' and char in mixermapdict:
                    mixerchan = mixermapdict[char.replace(' ','')]
                    mutes[mixerchan] = 0

            print('mutes: {0}'.format(mutes))
            # print('Entrances: {0}'.format(row['Entrances']))
            # print('Exits: {0}'.format(row['Exits']))
            field = row['OnStage'].replace(' ', '').replace('()', '').split(',')
            muteelementval = ''
            for muteval in mutes:
                muteelementval += '{0}:{1},'.format(muteval, mutes[muteval])
            muteelementval = muteelementval[:-1]
            newcueelements['Mutes'] = muteelementval
            # putcuefile(newdoc, newcueelements)
            OS_clean = re.sub(r'\(.*?\)', '', row['OnStage']).replace(' ','')
            En_clean = re.sub(r'\(.*?\)', '', row['Entrances']).replace(' ','')
            Ex_clean = re.sub(r'\(.*?\)', '', row['Exits']).replace(' ', '')
            print('Onstage: {0}, Entrances: {1}, Exits: {2}'.format(row['OnStage'], row['Entrances'], row['Exits']))
            newcueelements['OnStage'] = OS_clean
            newcueelements['Entrances'] = En_clean
            newcueelements['Exits'] = Ex_clean
            putcuefile(newdoc, newcueelements, cue_num)

    newdoctree = ET.ElementTree(newdoc)
    newdoctree.write('/home/mac/Shows/Fiddler/Fiddler_cuesx.xml')
    pass