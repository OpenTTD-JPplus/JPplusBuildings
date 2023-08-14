import pandas as pd
import codecs
import copy
import json
from colourdict import colourdict as colourdict
from lib import colourfunctions

colourfunctions.ImportColoursTab()

# create colour profiles and palette dictionaries
colour_profiles = raw_colour_profiles.copy()
palette = raw_colour_profiles.copy()

for b in colour_profile_names:
    colour_profiles[b] = {keys:values for keys, values in colour_profiles[b].items() if values != 0}

# get remap offsets
remap = colour_profiles['remap']

# delete palette lines
keys = ['palette01', 'palette02', 'palette03', 'palette04', 'palette05', 'palette06', 'palette07', 'palette08']
for key in keys:
    colour_profiles.pop(key, None)
    colour_profiles.pop('remap', None)

# create palette dictionary
for p in colour_profile_names:
    if p not in keys:
        palette.pop(p, None)
    else:
        pass


# create colour profile dictionaries
with open('colourprofiles.py', 'w') as f:
    f.write("\n# Colour Profiles\n")
    f.close()
for b in colour_profiles:
    with open('colourprofiles.py', 'a') as f:
        f.write("\n")
        f.write(str(b) + " = ")
        f.write(json.dumps(colour_profiles[b]))
        f.write("\n")
        f.close()

file1 = open('colourprofiles.py', 'r')
file2 = open('buildings.py', 'r')

# Read the contents of the text files
content1 = file1.read()
content2 = file2.read()

# Close the source text files
file1.close()
file2.close()

# Open the destination file
destination_file = open('colourprofiles.py', 'w')

# Write the concatenated content to the destination file
destination_file.write(content1 + content2)
# Close the destination file
destination_file.close()
