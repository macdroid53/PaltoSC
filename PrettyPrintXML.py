import os
from os import path
import sys
import uuid
import csv
import re
import inspect
import logging
import string


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


class indent:
    def __init__(self, indent_char='  '):
        self.level = 0
        self.indent_char = indent_char
    def inclevel(self):
        self.level += 1
    def declevel(self):
        self.level -= 1
    def getindent(self):
        return self.level * self.indent_char



bracketsets_re = re.compile('<.*?>')
endbracket_re = re.compile('<[/].*?>')
a = bracketsets_re.findall('<show_control><Cue num="000" uuid="f40e83e1-f69f-4fd7-bd22-5baae2d1fd07">')
b = bracketsets_re.findall('<CueCall>Come children..lets go.</CueCall><nn>')
c = endbracket_re.findall('<CueCall>"Come children..let\'s go."</CueCall><nn>')



endtag_re = re.compile('</[\w]*>')
onelinetag_re = re.compile('<.*?/>')
d = onelinetag_re.findall('<OnStage />')

commenttag_re = re.compile('<!--.*?-->')
e = commenttag_re.findall('<!--This a comment on a separate line-->')
emptytag_re = re.compile('></')
print(emptytag_re.search('<ccc></ccc>'))
print(emptytag_re.search('<ccc>x</ccc>'))

#print(endtag_re.search('</a>'))
bowtie_re = re.compile('><')
#print(bowtie_re.search('<cccc>bbb</a>'))
begendtag_re = re.compile('<[\w]*>[\w]*<') #</[\w]*>')
#print(begend_tag_re.search('<cccc>bbb</a>'))
#print(begtag_re.search('<CueCall>"Come children..let\'s go."</CueCall>'))
#print(endtag_re.search('<CueCall>"Come children..let\'s go."</CueCall>'))
#print(begendtag_re.search('<CueCall>"Come children..let\'s go."</CueCall>'))



f = open('/home/mac/Shows/Fiddler/Fiddler_cuesx.xml', 'r')
xml = f.read()
f.close()

# Removing old indendations
raw_xml = ''
for line in xml:
    if line == '\n' or line == '\t':
        pass
    else:
        raw_xml += line
#xml = raw_xml
new_xml = ''
new_line = ''
ind = indent()
for i in range((len(raw_xml))):
    new_line += raw_xml[i]
    brackets = bracketsets_re.findall(new_line)
    endbracket = endbracket_re.findall(new_line)
    onelinetag = onelinetag_re.findall(new_line)
    commenttag = commenttag_re.findall(new_line)
    if brackets.__len__() == 0:
        pass
    if brackets.__len__() == 1 and onelinetag.__len__() == 1:
        new_xml += ind.getindent() + new_line + "\n"
        new_line = ''
    elif brackets.__len__() == 1 and commenttag.__len__() == 1:
        new_xml += ind.getindent() + new_line + "\n"
        new_line = ''
    elif brackets.__len__() == 1 and endbracket.__len__() == 1:
        # this is a closing tag from some previous opening tag
        # decrement the indent and write
        ind.declevel()
        new_xml += ind.getindent() + new_line + "\n"
        new_line = ''
    elif brackets.__len__() == 2 and endbracket.__len__() == 1:
        # this is a complete tag, save it at the current indent level
        new_xml += ind.getindent() + new_line + "\n"
        new_line = ''
    elif brackets.__len__() == 2 and endbracket.__len__() == 0:
        if ind.level == 0:
            #this is two opening tags, write the first with the current indent
            new_xml += brackets[0] + '\n'
            # increment the indent and write the second
            ind.inclevel()
            new_xml += ind.getindent() + brackets[1] + '\n'
            new_line = ''
            ind.inclevel()
        else:
            # this is sequential two opening tags somewhere other than beginning of file
            #save the first
            new_xml += ind.getindent() + brackets[0] + '\n'
            # increment the level and use second a base for the next line
            ind.inclevel()
            new_line = brackets[1]
    # elif brackets.__len__() == 1 and endbracket.__len__() == 0:
    #     # this is a single open tag, save at current indent level
    #     new_xml += ind.getindent() + new_line + "\n"
    #     new_line = ''

    pass

f = open('/home/mac/Shows/Fiddler/Fiddler_cues_pretty.xml', 'w')
f.write(new_xml)
f.close()
