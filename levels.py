import pandas as pd
import codecs
import os
from colourprofiles import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

print("Running levels.py")

for b in buildings:
    levels_pnml = open("src/houses/" + b + "/levels/all.pnml", "wt")
    levels_pnml.write("\n// " + b + " levels\n")
    levels_pnml.close()
    levels = list(buildings_dict[b]["levels"])
    for l in levels:
        template = open("./src/houses/" + b + "/variants/all.pnml", "rt")
        current_level = open("./src/houses/" + b + "/levels/all.pnml", "a")
        for line in template:
            if l == 'sky' or l == "x":
                current_level.write(line.replace('_xL_', str('_')))
            else:
                current_level.write(line.replace('_xL_', str('_' + l +'_')))
        template.close()
        current_level.close()