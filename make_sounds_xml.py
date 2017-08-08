import os
from os import path
import sys
import uuid
import csv
import re
import inspect
import logging
try:
    from lxml import ET
except ImportError:
    import xml.etree.ElementTree as ET


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filename='ShowMixer.log', filemode='w',
                        format='%(name)s %(levelname)s %(message)s')
    logging.info('Begin')
    newdoc = ET.Element('show_control')
    directory = os.fsencode('/home/mac/Shows/WS1/sounds/background_music')
    soundsfile = open('/home/mac/Shows/WS1/sounds/WS_sounds.xml', 'w')
    soundsfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    soundsfile.write('<show_control>\n')
    soundsfile.write('  <sounds>\n')
    soundsfile.write('    <version>1.0</version>\n')

    for file_count, filename in enumerate(os.listdir(directory)):
        if filename.endswith(bytes('.wav', 'utf-8')):
            print('Num: {}: File Name: {}'.format(file_count, filename.decode('utf-8')))
            soundsfile.write('    <sound>\n')
            soundsfile.write('      <name>background-{:02}</name>\n'.format(file_count+1))
            soundsfile.write('      <wav_file_name>background_music/{}</wav_file_name>\n'.format(filename.decode('utf-8')))
            soundsfile.write('      <designer_volume_level>0.33</designer_volume_level>\n')
            soundsfile.write('      <designer_pan>0.00</designer_pan>\n')
            soundsfile.write('      <release_duration_time>1.0</release_duration_time>\n')
            soundsfile.write('    </sound>\n\n')

            continue
        else:
            continue
    soundsfile.write('    <routing></routing>\n')
    soundsfile.write('  </sounds>\n')
    soundsfile.write('</show_control>\n')
    soundsfile.close()
    pass