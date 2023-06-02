import pandas as pd
import codecs
import copy
from buildings import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

print("Running items.py")
print("Attempting items creation")

# convert into dataframe
df1 = pd.read_excel("docs/buildings.xlsx")

# convert into dictionary
dict = df1.to_dict()

name = list(dict["name"].values())
id = list(dict["id"].values())
tile_size = list(dict["tile_size"].values())
string_name = list(dict["stringname"].values())
population = list(dict["population"].values())
probability = list(dict["probability"].values())
substitute = list(dict["substitute"].values())
building_class = list(dict["building_class"].values())
yearstart = list(dict["yearstart"].values())
yearend = list(dict["yearend"].values())
minimum_lifetime = list(dict["minimum_lifetime"].values())
height = list(dict["height"].values())
townzones = list(dict["townzones"].values())
building_flags = list(dict["building_flags"].values())
graphics_default = list(dict["graphics_default"].values())
graphics_north = list(dict["graphics_north"].values())
graphics_east = list(dict["graphics_east"].values())
graphics_west = list(dict["graphics_west"].values())
graphics_south = list(dict["graphics_south"].values())
cargo_pass = list(dict["cargo_pass"].values())
cargo_mail = list(dict["cargo_mail"].values())
accepted_cargoes = list(dict["accepted_cargoes"].values())
con_check_override = list(dict["con_check_override"].values())

search_text_id = "_id_"
search_text_tile_size = "iXj"
search_text_string_name = "_stringname_"
search_text_population = "_population_"
search_text_probability = "_probability_"
search_text_substitute = "_substitute_"
search_text_building_class = "_building_class_"
search_text_yearstart = "_yearstart_"
search_text_yearend = "_yearend_"
search_text_minimum_lifetime = "_minimum_lifetime_"
search_text_height = "height"
search_text_con_check = "_con_check_"
search_text_townzones = "_townzones_"
search_text_building_flags = "_building_flags_"
search_text_graphics_default = "graphics_default_snow"
search_text_graphics_north = "graphics_north_snow"
search_text_graphics_east = "graphics_east_snow"
search_text_graphics_west = "graphics_west_snow"
search_text_graphics_south = "graphics_south_snow"
search_text_cargo_pass = "_cargo_pass_"
search_text_cargo_mail = "_cargo_mail_"
search_text_accepted_cargoes = "_accepted_cargoes_"

n = 0
for i in name:
	template = open("./src/templates/item_template.pnml", "rt")
	current_item = open("./src/items/" + i +".pnml", "wt")
	for line in template:
		current_item.write(line.replace('_name_', str('_' + i)))
	current_item.close()
	template.close()

	house_id = id[n]
	house_tile_size = tile_size[n]
	house_string_name = string_name[n]
	house_population = population[n]
	house_probability = probability[n]
	house_substitute = substitute[n]
	house_building_class = building_class[n]
	house_yearstart = yearstart[n]
	house_yearend = yearend[n]
	house_minimum_lifetime = minimum_lifetime[n]
	house_height = height[n]
	house_con_check = height[n]
	house_con_check_override = con_check_override[n]
	house_townzones = townzones[n]
	house_building_flags = building_flags[n]
	house_graphics_default = graphics_default[n] + "_sprites"
	house_graphics_north = graphics_north[n] + "_sprites"
	house_graphics_east = graphics_east[n] + "_sprites"
	house_graphics_west = graphics_west[n] + "_sprites"
	house_graphics_south = graphics_south[n] + "_sprites"
	house_cargo_pass = cargo_pass[n]
	house_cargo_mail = cargo_mail[n]
	house_accepted_cargoes = accepted_cargoes[n]
	with open(r'./src/items/' + name[n] +'.pnml', 'r') as file:
		data = file.read()
		data = data.replace(search_text_id, str(house_id))
		data = data.replace(search_text_tile_size, str(house_tile_size))
		data = data.replace(search_text_string_name, str(house_string_name))
		data = data.replace(search_text_population, str(house_population))
		data = data.replace(search_text_probability, str(house_probability))
		data = data.replace(search_text_substitute, str(house_substitute))
		data = data.replace(search_text_building_class, str(house_building_class))
		data = data.replace(search_text_yearstart, str(house_yearstart))
		data = data.replace(search_text_yearend, str(house_yearend))
		data = data.replace(search_text_minimum_lifetime, str(house_minimum_lifetime))	
		data = data.replace(search_text_townzones, str(house_townzones))
		data = data.replace(search_text_building_flags, str(house_building_flags))
		data = data.replace(search_text_graphics_default, str(house_graphics_default))
		data = data.replace(search_text_graphics_north, str(house_graphics_north))
		data = data.replace(search_text_graphics_east, str(house_graphics_east))
		data = data.replace(search_text_graphics_west, str(house_graphics_west))
		data = data.replace(search_text_graphics_south, str(house_graphics_south))
		data = data.replace(search_text_cargo_pass, str(house_cargo_pass))
		data = data.replace(search_text_cargo_mail, str(house_cargo_mail))
		data = data.replace(search_text_accepted_cargoes, str(house_accepted_cargoes))
		if con_check_override[n] == "standard":
			data = data.replace(search_text_con_check, str(house_con_check))
		else:
			data = data.replace(search_text_con_check, str(house_con_check_override))

	with open(r'./src/items/' + name[n] + '.pnml', 'w') as file:
		file.write(data)
		#get list of lines
	a_file = open(r'./src/items/' + name[n] +'.pnml', 'r')
	lines = a_file.readlines()
	a_file.close()
	new_file = open(r'./src/items/' + name[n] + '.pnml', 'w')
	for line in lines:

		#delete line matching string
		if line.find('none') == -1:
			new_file.write(line)

	new_file.close()

	n = n+1

# ADD PARAMETER TO RELEVANT BUILDINGS

item_param_buildings = copy.deepcopy(buildings)
for b in buildings:
    try: 
        buildings_dict[b]["item_param_enclosure_top"] != None     
    except:
        item_param_buildings.remove(b)

for b in item_param_buildings:
	top =  buildings_dict[b]["item_param_enclosure_top"]
	bottom =  buildings_dict[b]["item_param_enclosure_bottom"]
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
for i in name:
    append_variants(i)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(items_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()

print("Items created")