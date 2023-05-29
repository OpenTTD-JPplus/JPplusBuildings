
from buildings import buildings_dict as buildings_dict
import copy
import os

buildings = list(buildings_dict.keys())

print("Running pnml_combiner.py")

# Delete files for those that are manual overriden

folders = ["levels", "colours", "variants"]

manual_gfx = copy.deepcopy(buildings)
manual_switches = copy.deepcopy(buildings)
for b in buildings:
    try:
        buildings_dict[b]["manual_gfx"] == True
    except:
        manual_gfx.remove(b)
    try:
        buildings_dict[b]["manual_switches"] == True
    except:
        manual_switches.remove(b)

for b in manual_gfx:
    for f in folders:
        folder = './src/houses/' + b +'/' + f + '/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

for b in manual_switches:
    if os.path.exists('./src/houses/' + b +'/switches/colour_switches.pnml'):
        os.remove('./src/houses/' + b +'/switches/colour_switches.pnml')
    else:
        pass

# Create each buildings pnml file list

for b in buildings:
    variants = list(buildings_dict[b]["variants"].keys())
    f = open("./src/houses/" + b + "/" + b +".pnml", "w")
    f.write("\n// " + b + "\n")
    #Sprites
    f.write('\n#include "src/houses/' + b +'/gfx/' + b + '_sprites.pnml"')
    # Levels
    if os.path.exists('./src/houses/' + b +'/levels/all.pnml'):
        f.write('\n#include "src/houses/' + b +'/levels/all.pnml"')
    else:
        pass
    # Colour Switches
    if os.path.exists('./src/houses/' + b +'/switches/colour_switches.pnml'):
        f.write('\n#include "src/houses/' + b +'/switches/colour_switches.pnml"')
    elif os.path.exists('./src/houses/' + b +'/switches/manual_switches.pnml'):
        f.write('\n#include "src/houses/' + b +'/switches/manual_switches.pnml"')
    else:
        print(b + " doesn't have a switches file")
    # Directional switches
    if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
        pass
    elif variants == ['a', 'b']: 
        f.write('\n#include "src/houses/' + b +'/switches/direction_switches.pnml"')
    else:
        print(b + " has an unrecognised variant #4 pnml_combiner.py")
    f.close()
