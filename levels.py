import pandas as pd
import codecs
import os
from buildings import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

print("Running levels.py")

for b in buildings:
    levels = list(buildings_dict[b]["levels"])
    for l in levels:
        template = open("./src/houses/" + b + "/variants/all.pnml", "rt")
        current_level = open("./src/houses/" + b + "/levels/" + l +".pnml", "wt")
        for line in template:
            if l == 'sky' or l == "x":
                current_level.write(line.replace('_xL_', str('_')))
            else:
                current_level.write(line.replace('_xL_', str('_' + l +'_')))
        template.close()
        current_level.close()

# COMBINE THE LEVELS INTO AN 'ALL' FILE

# Cycle through each building and combine each of it's levels
for b in buildings:
    sections = []
    levels = list(buildings_dict[b]["levels"])
    for l in levels:
        levels_pnml_path = "src/houses/" + b + "/levels/all.pnml"
        filename = "src/houses/" + b + "/levels/" + l + ".pnml"
        stuff = codecs.open(filename.format(l),'r','utf8')
        sections.append(stuff.read())
        stuff.close()
        processed_pnml_file = codecs.open(levels_pnml_path,'w','utf8')
        processed_pnml_file.write('\n'.join(sections))
        processed_pnml_file.close()
