import pandas as pd
import codecs
import json
from lib import colourfunctions

print("Running colours.py")

colourfunctions.ImportColoursTab()
colourfunctions.CreateColourFiles()

'''import colourprofiles
from colourprofiles import buildings_dict as buildings_dict
from lib.remap import remap as remap

buildings = list(buildings_dict.keys())



# COMBINE THE COLOURS INTO AN 'ALL' FILE

# Cycle through each building and combine each of it's colours
for b in buildings:
    sections = []
    colours = list(buildings_dict[b]["colours"].keys())
    for c in colours:
        colours_pnml_path = "src/houses/" + b + "/colours/all.pnml"
        filename = "src/houses/" + b + "/colours/" + c + ".pnml"
        stuff = codecs.open(filename.format(file),'r','utf8')
        sections.append(stuff.read())
        stuff.close()
        processed_pnml_file = codecs.open(colours_pnml_path,'w','utf8')
        processed_pnml_file.write('\n'.join(sections))
        processed_pnml_file.close()'''