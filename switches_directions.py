
from buildings import buildings_dict as buildings_dict
import codecs
import os

buildings = list(buildings_dict.keys())

print("Running switches_directions.py")

# Create a spritedirection file for relevant buildings
for b in buildings:
    heights = list(buildings_dict[b]["heights"])
    variants = list(buildings_dict[b]["variants"].keys())
    if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
        pass
    elif variants == ['a', 'b']:    
        for h in heights:
            with open(r'./src/templates/spritedirections_ab.pnml', 'r') as file:    
                data = file.read()
                data = data.replace("building_name", b)
                data = data.replace("height", h)
            with open(r'./src/houses/' + b + '/switches/' + h + '.pnml', 'w') as file:
                file.write(data)
                file.close()
    elif variants == ['a', 'b', 'c']:    
        for h in heights:
            with open(r'./src/templates/spritedirections_abc.pnml', 'r') as file:    
                data = file.read()
                data = data.replace("building_name", b)
                data = data.replace("height", h)
            with open(r'./src/houses/' + b + '/switches/' + h + '.pnml', 'w') as file:
                file.write(data)
                file.close()
    else:
        print(b + " has an unrecognised variant #1")

# Combine into other switches file
for b in buildings:
    sections = []
    heights = list(buildings_dict[b]["heights"])
    variants = list(buildings_dict[b]["variants"].keys())
    if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
        pass
    elif variants == ['a', 'b'] or variants == ['a', 'b', 'c']: 
        for h in heights:
            destination_pnml_path = "src/houses/" + b + "/switches/direction_switches.pnml"
            filename = "src/houses/" + b + "/switches/" + h + ".pnml"
            stuff = codecs.open(filename.format(h),'r','utf8')
            sections.append(stuff.read())
            stuff.close()
            processed_pnml_file = codecs.open(destination_pnml_path,'w','utf8')
            processed_pnml_file.write('\n'.join(sections))
            processed_pnml_file.close()
    else:
        print(b + " has an unrecognised variant #2")

# Delete variant files
for b in buildings:
    heights = list(buildings_dict[b]["heights"])
    variants = list(buildings_dict[b]["variants"].keys())
    if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
        pass
    elif variants == ['a', 'b'] or variants == ['a', 'b', 'c']:
        for h in heights:    
            file_path = "src/houses/" + b + "/switches/" + h + ".pnml"
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error: %s : %s" % (file_path, e.strerror))
    else:
        print(b + " has an unrecognised variant #3")