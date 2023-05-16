import pandas as pd
import codecs
import os
from buildings import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

m = 0
for b in buildings:
    levels = list(buildings_dict[buildings[m]]["levels"])
    n = 0
    for l in levels:
        template = open("./src/houses/" + buildings[m] + "/variants/all.pnml", "rt")
        current_level = open("./src/houses/" + buildings[m] + "/levels/" + levels[n] +".pnml", "wt")
        for line in template:
            current_level.write(line.replace('_xL_', str('_' + levels[n] +'_')))
        template.close()
        current_level.close()
        n = n+1
    m = m+1

# COMBINE THE COLOURS INTO AN 'ALL' FILE

# Cycle through each building and combine each of it's colours
m = 0
for b in buildings:
    sections = []
    levels = list(buildings_dict[buildings[m]]["levels"])
    n = 0
    for l in levels:
        levels_pnml_path = "src/houses/" + buildings[m] + "/levels/all.pnml"
        filename = "src/houses/" + buildings[m] + "/levels/" + levels[n] + ".pnml"
        stuff = codecs.open(filename.format(l),'r','utf8')
        sections.append(stuff.read())
        stuff.close()
        n = n + 1
        processed_pnml_file = codecs.open(levels_pnml_path,'w','utf8')
        processed_pnml_file.write('\n'.join(sections))
        processed_pnml_file.close()
    m = m+1
