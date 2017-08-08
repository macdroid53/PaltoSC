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
                        filename='make_sound_sequences_xml.log', filemode='w',
                        format='%(name)s %(levelname)s %(message)s')
    logging.info('Begin')
    directory = os.fsencode('/home/mac/Shows/WS1/sounds/background_music')
    soundsfile = open('/home/mac/Shows/WS1/sounds/WS_sounds_seqitems.xml', 'w')
    # soundsfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    # soundsfile.write('<show_control>')
    # soundsfile.write('<sounds>')
    # soundsfile.write('<version>1.0</version>')

    for file_count, filename in enumerate(os.listdir(directory)):
        if filename.endswith(bytes('.wav', 'utf-8')):
            print('Num: {}: File Name: {}'.format(file_count, filename.decode('utf-8')))
            soundsfile.write('    <sequence_item>\n')
            soundsfile.write('      <name>play_background_{:02}</name>\n'.format(file_count+ 1))
            soundsfile.write('      <type>start_sound</type>\n'.format(filename.decode('utf-8')))
            soundsfile.write('      <sound_name>background-{:02}</sound_name>\n'.format(file_count + 1))
            soundsfile.write('      <cluster_number>0</cluster_number>\n')
            soundsfile.write('      <tag>background</tag>\n')
            soundsfile.write('      <text_to_display>Pre Show Music</text_to_display>\n')
            soundsfile.write('      <next_completion>play_background_{:02}</next_completion>\n'.format(file_count + 2))
            soundsfile.write('      <time_to_wait>0.5</time_to_wait>\n')
            soundsfile.write('    </sequence_item>\n\n')

            continue
        else:
            continue
    soundsfile.close()
    pass