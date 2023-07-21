import pandas as pd
import codecs
from buildings import buildings_dict as buildings_dict

coloursdict = {
"white": 		"0",
"grey": 		"1",
"brown1": 		"2",
"brown2": 		"3",
"mauve":		"4",
"dark_green":	"5",
"peach":		"6",
"pink":			"7",
"light_blue":	"8",
"dark_blue":	"9",
"light_green":	"10",
"black":		"11",
"gold":			"12",
"red_brown":	"13",
"red":			"14",
"midgrey":      "15",
"mix01":        "16",
"mix02":        "17",
}

buildings = list(buildings_dict.keys())

print("Running colours.py")

# CREATE THE COLOUR SPRITELAYOUTS IN EACH BUILDING'S FOLDER

for b in buildings:
    colours = list(buildings_dict[b]["colours"].keys())
    for c in colours:
        template = open("./src/templates/colour_template.pnml", "rt")
        current_colour = open("./src/houses/" + b + "/colours/" + c +".pnml", "wt")
        for line in template:
            current_colour.write(line.replace('_clr_', str('_' + c +'_')))
        template.close()
        current_colour.close()

        search_text_remap = "_c_"
        search_text_ground = "spr_building_name_v_ground"
        search_text_ground_snow = "spr_building_name_v_ground_snow"
        search_text_building = "spr_building_name_v_xL_norm"
        search_text_building_snow = "spr_building_name_v_xL_snow"
        search_text_building_name = "building_name"
        recolour_remap = coloursdict[c]
        with open(r'./src/houses/' + b + '/colours/' + c +'.pnml', 'r') as file:
            data = file.read()
            try:
                ground_sprite = buildings_dict[b]["ground"]
                data = data.replace(search_text_ground_snow, ground_sprite)
                data = data.replace(search_text_ground, ground_sprite)            
            except:
                pass
            try:
                building_sprite = buildings_dict[b]["building"]
                data = data.replace(search_text_building_snow, building_sprite + "_snow")
                data = data.replace(search_text_building, building_sprite + "_norm")  
            except:
                pass
            data = data.replace(search_text_remap, recolour_remap)
            data = data.replace(search_text_building_name, b)
        with open(r'./src/houses/' + b+ '/colours/' + c + '.pnml', 'w') as file:
            file.write(data)

# COMBINE THE COLOURS INTO AN 'ALL' FILE

# Cycle through each building and combine each of it's colours
m = 0
for b in buildings:
    sections = []
    colours = list(buildings_dict[buildings[m]]["colours"].keys())
    n = 0
    for c in colours:
        colours_pnml_path = "src/houses/" + buildings[m] + "/colours/all.pnml"
        filename = "src/houses/" + buildings[m] + "/colours/" + colours[n] + ".pnml"
        stuff = codecs.open(filename.format(file),'r','utf8')
        sections.append(stuff.read())
        stuff.close()
        n = n + 1
        processed_pnml_file = codecs.open(colours_pnml_path,'w','utf8')
        processed_pnml_file.write('\n'.join(sections))
        processed_pnml_file.close()
    m = m+1
