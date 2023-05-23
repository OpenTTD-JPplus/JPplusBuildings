
from buildings import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

for b in buildings:
    variants = list(buildings_dict[b]["variants"].keys())
    f = open("./src/houses/" + b + "/" + b +".pnml", "w")
    f.write("\n// " + b + "\n")
    f.write('\n#include "src/houses/' + b +'/gfx/' + b + '_sprites.pnml"')
    f.write('\n#include "src/houses/' + b +'/levels/all.pnml"')
    f.write('\n#include "src/houses/' + b +'/switches/colour_switches.pnml"')
    if variants == ['x']:
        pass
    elif variants == ['a', 'b']: 
        f.write('\n#include "src/houses/' + b +'/switches/direction_switches.pnml"')
    else:
        print("Other")
    f.close()
