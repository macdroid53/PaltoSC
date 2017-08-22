import os
from os import path
import sys
import uuid
import csv
import re
import inspect
import logging
import string
try:
    from lxml import ET
except ImportError:
    import xml.etree.ElementTree as ET

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(currentdir)
syblingdir =  os.path.dirname(currentdir) + '/ShowControl/ShowControl/utils'
print(syblingdir)
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0,syblingdir)
sys.path.insert(0,'/home/mac/SharedData/PycharmProjs/ShowControl/ShowMixer')
print(sys.path)

from Show import Show
from ShowConf import ShowConf
from ShowControlConfig import configuration, CFG_DIR, CFG_PATH
from MixerConf import MixerConf


def sort_controls(self, control_list=[]):
    chlist = []
    auxlist = []
    buslist = []
    mainlist = []
    for control in control_list:
        if 'bus' in control:
            buslist.append(control)
        elif 'aux' in control:
            auxlist.append(control)
        elif 'main' in control:
            mainlist.append(control)
        elif 'ch' in control:
            chlist.append(control)
    buslist = sorted(buslist)
    auxlist = sorted(auxlist)
    mainlist = sorted(mainlist)
    chlist = sorted(chlist)
    sorted_controls = chlist + auxlist + buslist + mainlist
    return sorted_controls


firstuuid = ''
def getmixermap(mapfile):
    global firstuuid
    mixermap = ET.parse(mapfile)
    mixermap_root = mixermap.getroot()
    firstmap = mixermap_root.find('mixermap')
    firstuuid = firstmap.get('uuid')
    charcount = int(firstmap.get('charcount'))

    chars = firstmap.findall('input')
    chardict = {}
    for char in chars:
        cnum = int(char.attrib['chan'])
        mxrid = int(char.attrib['mixerid'])
        char = char.attrib['char']
        chardict[char] = 'M{0:1}ch{1:02}'.format(mxrid, cnum)
    return chardict

def putcuefile(newdoc, cuedict, cuenum):
    global firstuuid
    if firstuuid and cuenum == 0:
        cueele = ET.SubElement(newdoc, 'Cue', {'uuid': '{0}'.format(firstuuid), 'num': '{0:003}'.format(cuenum)})
        firstuuid = None
    else:
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

def sort_controls(control_str=''):
    control_list = control_str.split(',')
    chlist = []
    auxlist = []
    buslist = []
    mainlist = []
    for control in control_list:
        if 'bus' in control:
            buslist.append(control)
        elif 'aux' in control:
            auxlist.append(control)
        elif 'main' in control:
            mainlist.append(control)
        elif 'ch' in control:
            chlist.append(control)
    buslist = sorted(buslist)
    auxlist = sorted(auxlist)
    mainlist = sorted(mainlist)
    chlist = sorted(chlist)
    sorted_controls = chlist + auxlist + buslist + mainlist
    return sorted_controls


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filename='CVCS2XML.log', filemode='w',
                        format='%(name)s %(levelname)s %(message)s')
    logging.info('Begin')
    cfg = configuration()
    mixers = {}
    show_conf = ShowConf(cfg.cfgdict)
    for mxrid in show_conf.equipment['mixers']:
        # print(mxrid)
        if show_conf.equipment['mixers'][mxrid]['IP_address']:
            mixeraddress = show_conf.equipment['mixers'][mxrid]['IP_address'] + ',' + \
                           show_conf.equipment['mixers'][mxrid]['port']
        else:
            mixeraddress = show_conf.equipment['mixers'][mxrid]['MIDI_address']
        mixers[mxrid] = MixerConf(path.abspath(path.join(CFG_DIR, cfg.cfgdict['configuration']['mixers']['folder'],
                                                              cfg.cfgdict['configuration']['mixers']['file'])),
                                       show_conf.equipment['mixers'][mxrid]['mfr'],
                                       show_conf.equipment['mixers'][mxrid]['model'],
                                       mixeraddress)
    chan_name_list = list(a['name'].lower() for a in mixers[0].mxrconsole)
    level_list = []
    for count, chan in enumerate(chan_name_list):
        level_list.append('M{0}{1}:0'.format(0,chan))
    level_val = ','.join(level_list)
    mixermapdict = getmixermap('/home/mac/Shows/Fiddler/MixerMap_full.xml')
    mutes = {}
    for chan in chan_name_list:
        print('Chan Name: {}'.format(chan))
        mxrchnnam = 'M{0}{1}'.format(0,chan)
        mutes[mxrchnnam] = 0
    # for chan in mixermapdict:
    #     print('Char: {0} Chan: {1}'.format(chan, mixermapdict[chan]))
    #     mutes[mixermapdict[chan]] = 0
    # newdoc = ET.Element('show_control')
    templatedoc = ET.parse('/home/mac/Shows/Fiddler/Template_cues.xml')
    newdoc = templatedoc.getroot()
    templatecues = newdoc.findall('./Cue')
    cue_num_offset = len(templatecues)
    with open('/home/mac/Shows/Fiddler/Fiddler_katie_txt-1.csv', newline='') as f:
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
                if char not in mixermapdict and char != '':
                    print('{0} not found!'.format(ent))
                    logging.info('In {} Entrances char: {} not found!'.format(row['Id'],char))
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
                if char not in mixermapdict and char != '':
                    print('{0} not found!'.format(xit))
                    logging.info('In {} Exits char: {} not found!'.format(row['Id'],char))
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
            mutes_sorted = sort_controls( muteelementval )
            newcueelements['Mutes'] = ','.join(mutes_sorted)
            # add dummy <levels> element
            newcueelements['Levels'] = level_val

            OS_clean = re.sub(r'\(.*?\)', '', row['OnStage']).replace(' ','')
            En_clean = re.sub(r'\(.*?\)', '', row['Entrances']).replace(' ','')
            Ex_clean = re.sub(r'\(.*?\)', '', row['Exits']).replace(' ', '')
            print('Onstage: {0}, Entrances: {1}, Exits: {2}'.format(row['OnStage'], row['Entrances'], row['Exits']))
            newcueelements['OnStage'] = OS_clean
            newcueelements['Entrances'] = En_clean
            newcueelements['Exits'] = Ex_clean
            putcuefile(newdoc, newcueelements, cue_num + cue_num_offset)

    newdoctree = ET.ElementTree(newdoc)
    newdoctree.write('/home/mac/Shows/Fiddler/Fiddler_cuesx_txt-1.xml')

    pass