map_cue_dict = {'000':'0', '056':'1', '072':'2', '074':'3', '083':'4', '118':'5'} # {cue_num:mapnum}
newfile = open('/home/mac/Shows/Fiddler/Fiddler_cuesx_map.xml', newline='', mode='w')
with open('/home/mac/Shows/Fiddler/Fiddler_cuesx.xml', newline='') as f:
    lines = f.readlines()
    for line in lines:
        if '<Cue ' in line:
            num_idx = line.find('num="')
            cue_num = line[num_idx + 5:num_idx + 8]
            #print('idx: {}, Cue num: {}'.format(num_idx, cue_num))
            if cue_num in map_cue_dict.keys():
                map_count = map_cue_dict[cue_num]
        if '</Cue>' in line:
            print('    <map>{}</map>\n'.format(map_count))
            newfile.write('    <map>{}</map>\n'.format(map_count))
        print(line, end='')
        newfile.write(line)
        # else:
        #     print(line, end='')
newfile.close()