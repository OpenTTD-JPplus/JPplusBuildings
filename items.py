import pandas as pd
import os, shutil
import codecs
import copy
from buildings import buildings_dict as buildings_dict

# convert excel spreadsheet into dataframe
df1 = pd.read_excel('docs/buildings.xlsx','items')

# convert dataframe into dictionary
all_buildings = df1.set_index('name').T.to_dict('dict')

# create active, inactive and parameter building lists
active_buildings = []
inactive_buildings = []
parameter_buildings = []
for b in all_buildings:
    if  all_buildings[b]["include"] == False:
        inactive_buildings.append(b)
    else:
        active_buildings.append(b)
    # parameter list
    if  all_buildings[b]["param_top"] == "none":
        pass
    else:
        parameter_buildings.append(b)


folders = list(df1["folder"])
folders = list(dict.fromkeys(folders))

f = open("./src/houses.pnml", "w")
f.write('\n// House pnml files\n')
f.close()
for b in folders:
    f = open("./src/houses.pnml", "a")
    f.write('\n#include "src/houses/' + b + '/' + b + '.pnml"')
    f.close()

# delete out items folder before starting
folder = './src/items/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

for b in active_buildings:
    # Create the files
    template = open("./src/templates/item_template.pnml", "rt")
    current_item = open("./src/items/" + b +".pnml", "wt")
    for line in template:
        current_item.write(line.replace('_name_', str('_' + b)))
    current_item.close()
    template.close()
    # Replace the placeholders with data from spreadsheet
    with open(r'./src/items/' + b +'.pnml', 'r') as file:
        data = file.read()
        data = data.replace('_id_', str(all_buildings[b]["id"]))
        data = data.replace('iXj', str(all_buildings[b]["tile_size"]))
        data = data.replace('_stringname_', str(all_buildings[b]["stringname"]))
        data = data.replace('_population_', str(all_buildings[b]["population"]))
        data = data.replace('_probability_', str(all_buildings[b]["probability"]))
        data = data.replace('_substitute_', str(all_buildings[b]["substitute"]))
        data = data.replace('_building_class_', str(all_buildings[b]["building_class"]))
        data = data.replace('_yearstart_', str(all_buildings[b]["yearstart"]))
        data = data.replace('_yearend_', str(all_buildings[b]["yearend"]))
        data = data.replace('_minimum_lifetime_', str(all_buildings[b]["minimum_lifetime"]))
        data = data.replace('height', str(all_buildings[b]["height"]))
        data = data.replace('_townzones_', str(all_buildings[b]["townzones"]))
        data = data.replace('_building_flags_', str(all_buildings[b]["building_flags"]))
        data = data.replace('graphics_default_snow', str(all_buildings[b]["graphics_default"]) + "_sprites")
        data = data.replace('graphics_north_snow', str(all_buildings[b]["graphics_north"]) + "_sprites")
        data = data.replace('graphics_east_snow', str(all_buildings[b]["graphics_east"]) + "_sprites")
        data = data.replace('graphics_west_snow', str(all_buildings[b]["graphics_west"]) + "_sprites")
        data = data.replace('graphics_south_snow', str(all_buildings[b]["graphics_south"]) + "_sprites")
        data = data.replace('_cargo_pass_', str(all_buildings[b]["cargo_pass"]))
        data = data.replace('_cargo_mail_', str(all_buildings[b]["cargo_mail"]))
        data = data.replace('_accepted_cargoes_', str(all_buildings[b]["accepted_cargoes"]))
        
        if all_buildings[b]["con_check_override"] == "standard":
            data = data.replace('_con_check_', str(all_buildings[b]["height"]))
        else:
            data = data.replace('_con_check_', str(all_buildings[b]["con_check_override"]))
    
    with open(r'./src/items/' + b + '.pnml', 'w') as file:
        file.write(data)
    a_file = open(r'./src/items/' + b +'.pnml', 'r')
    lines = a_file.readlines()
    a_file.close()
    new_file = open(r'./src/items/' + b + '.pnml', 'w')
    for line in lines:
        #delete line matching string
        if line.find('none') == -1:
            new_file.write(line)
    new_file.close()
            
# Add Parameter to relevant buildings

for b in parameter_buildings:
	top =  all_buildings[b]["param_top"]
	bottom =  all_buildings[b]["param_bottom"]
	with open('./src/items/' + b + '.pnml', 'r+') as file: 
		file_data = file.read()
		file.seek(0, 0)
		file.write(top + '\n' + file_data) 
		file.close()
	with open('./src/items/' + b + '.pnml', 'a') as file: 
		file.write('\n' + bottom)
		file.close()

# MERGE THE ITEMS

# File with combined output
items_pnml_path = "./src/items.pnml"

# Create an empty list where all the PNML code will be placed
sections = []

# Function for copying code from .pnml files
def append_variants(file):
    filename = "./src/items/{}.pnml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    sections.append(stuff.read())
    stuff.close()

# Append header stuff which should always be first
for b in active_buildings:
    append_variants(b)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(items_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()

print("Items created")