
# Hirata

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
"midgrey":		"15"
}

building_name = "hirata"
colours = ["white", "grey", "mauve", "brown1", "brown2", "dark_green", "peach", "pink", "light_blue", "dark_blue"]
levels = ["3L", "4L", "5L", "6L"]
items = {
	"s" : {
		"height1" : "3L",
		"height2" : "4L"
	}, 
	"m" : {
		"height1" : "5L",
		"height2" : "6L"
	}
}
variants = {
    "a" : {
		"xoffset" : "0",
		"yoffset" : "0"
	},
	"b" : {
		"xoffset" : "0",
		"yoffset" : "0"
	}
  }
switches_required = True
iterate_switches_on_item = True 
variant_names = list(variants.keys())
item_names = list(items.keys())

# 1) Create the colours		
# 2) Merge the colours		
# 3) Create the variants	
# 4) Merge the variants 	
# 5) Create the levels		

# 1) CREATE THE COLOURS

n = 0
for i in colours:
	template = open("./colours/colour_template.pnml", "rt")
	current_colour = open("./colours/" + colours[n] +".pnml", "wt")
	for line in template:
		current_colour.write(line.replace('_clr_', str('_' + colours[n] +'_')))
	template.close()
	current_colour.close()

	search_text = "_c_"
	recolour_remap = coloursdict[i]
	with open(r'./colours/' + colours[n] +'.pnml', 'r') as file:
		data = file.read()
		data = data.replace(search_text, recolour_remap)
	with open(r'./colours/' + colours[n] + '.pnml', 'w') as file:
		file.write(data)
	n = n+1

# 2) COMBINE THE COLOURS

import codecs
import os

# File with combined output
colours_pnml_path = "colours/all.pnml"

# Create an empty list where all the PNML code will be placed
sections = []

# Function for copying code from .pnml files
def append_code(file):
    filename = "colours/{}.pnml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    sections.append(stuff.read())
    stuff.close()

# Append header stuff which should always be first
for i in colours:
    append_code(i)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(colours_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()

# 3) CREATE THE DIRECTION / VARIANTS

n = 0
for i in variants:
	all_colours = open("./colours/all.pnml", "rt")
	current_variant = open("./variants/" + variant_names[n] +".pnml", "wt")
	for line in all_colours:
		current_variant.write(line.replace('_v_', str('_' + variant_names[n] + '_')))
	current_variant.close()
	all_colours.close()

	search_text_x = "_xoff_"
	search_text_y = "_yoff_"
	xoff = variants[i]["xoffset"]
	yoff = variants[i]["yoffset"]
	with open(r'./variants/' + variant_names[n] +'.pnml', 'r') as file:
		data = file.read()
		data = data.replace(search_text_x, xoff)
		data = data.replace(search_text_y, yoff)
	with open(r'./variants/' + variant_names[n] + '.pnml', 'w') as file:
		file.write(data)
	n = n+1

# 4) MERGE THE DIRECTION / VARIANTS

# File with combined output
variants_pnml_path = "./levels/xL.pnml"

# Create an empty list where all the PNML code will be placed
sections = []

# Function for copying code from .pnml files
def append_variants(file):
    filename = "./variants/{}.pnml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    sections.append(stuff.read())
    stuff.close()

# Append header stuff which should always be first
for i in variants:
    append_variants(i)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()

# 5) CREATE THE LEVELS

n = 0
for i in levels:
	level_template = open("./levels/xL.pnml", "rt")
	current_level = open("./levels/" + levels[n] +".pnml", "wt")
	for line in level_template:
		current_level.write(line.replace('_xL_', str('_'+ levels[n] +'_')))
	current_level.close()
	level_template.close()
	n = n+1

print(building_name + " spritesets created")

# 1) CREATE THE DIRECTION / VARIANTS

n = 0
for i in variants:
	switch_template = open("./switches/template_rs.pnml", "rt")
	current_variant = open("./switches/" + variant_names[n] +".pnml", "wt")
	for line in switch_template:
		current_variant.write(line.replace('_v_', str('_' + variant_names[n] + '_')))
	current_variant.close()
	switch_template.close()
	n = n+1

# 2) MERGE THE DIRECTION / VARIANTS

# File with combined output
variants_pnml_path = "./switches/combined_variants.pnml"

# Create an empty list where all the PNML code will be placed
sections = []

# Function for copying code from .pnml files
def append_variants(file):
    filename = "./switches/{}.pnml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    sections.append(stuff.read())
    stuff.close()

# Append header stuff which should always be first
for i in variants:
    append_variants(i)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()

# 3) CREATE THE LEVELS

if iterate_switches_on_item == True:

	n = 0
	for i in items:
		items_template = open("./switches/combined_variants.pnml", "rt")
		current_item = open("./switches/" + item_names[n] +"_rs.pnml", "wt")
		for line in items_template:
			current_item.write(line.replace('_item_', str('_'+ item_names[n] +'_')))
		current_item.close()
		items_template.close()

		search_text_h1 = "height1"
		search_text_h2 = "height2"
		h1 = items[i]["height1"]
		h2 = items[i]["height2"]
		with open(r'./switches/' + item_names[n] +'_rs.pnml', 'r') as file:
			data = file.read()
			data = data.replace(search_text_h1, h1)
			data = data.replace(search_text_h2, h2)
		with open(r'./switches/' + item_names[n] + '_rs.pnml', 'w') as file:
			file.write(data)
		n = n+1

else:

	n = 0
	for i in levels:
		level_template = open("./switches/combined_variants.pnml", "rt")
		current_level = open("./switches/" + levels[n] +"_rs.pnml", "wt")
		for line in level_template:
			current_level.write(line.replace('_xL_', str('_'+ levels[n] +'_')))
		current_level.close()
		level_template.close()
		n = n+1

# 4) MERGE THE LEVELS

# File with combined output
variants_pnml_path = "./switches/combined_rs.pnml"

# Create an empty list where all the PNML code will be placed
sections = []

# Function for copying code from .pnml files
def append_variants(file):
    filename = "./switches/{}_rs.pnml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    sections.append(stuff.read())
    stuff.close()

# Append header stuff which should always be first

if iterate_switches_on_item == True:
	for i in items:
		append_variants(i)
else:
	for i in levels:
		append_variants(i)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()

print(building_name + " random switches created")

if switches_required == True:

	# 1) CREATE THE LEVELS

	if iterate_switches_on_item == True:

		n = 0
		for i in items:
			item_template = open("./switches/template_sw.pnml", "rt")
			current_item = open("./switches/" + item_names[n] +"_sw.pnml", "wt")
			for line in item_template:
				current_item.write(line.replace('_xL_', str('_'+ item_names[n] +'_')))
			current_item.close()
			item_template.close()
			n = n+1

		# 4) MERGE THE LEVELS

		# File with combined output
		variants_pnml_path = "./switches/combined_sw.pnml"

		# Create an empty list where all the PNML code will be placed
		sections = []

		# Function for copying code from .pnml files
		def append_variants(file):
			filename = "./switches/{}_sw.pnml"
			stuff = codecs.open(filename.format(file),'r','utf8')
			sections.append(stuff.read())
			stuff.close()

		# Append header stuff which should always be first
		for i in items:
			append_variants(i)

		# Write the content of 'sections' into a file and save it
		processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
		processed_pnml_file.write('\n'.join(sections))
		processed_pnml_file.close()

		print(building_name + " switches created using items")	

	else:

		n = 0
		for i in levels:
			level_template = open("./switches/template_sw.pnml", "rt")
			current_level = open("./switches/" + levels[n] +"_sw.pnml", "wt")
			for line in level_template:
				current_level.write(line.replace('_xL_', str('_'+ levels[n] +'_')))
			current_level.close()
			level_template.close()
			n = n+1

		# 4) MERGE THE LEVELS

		# File with combined output
		variants_pnml_path = "./switches/combined_sw.pnml"

		# Create an empty list where all the PNML code will be placed
		sections = []

		# Function for copying code from .pnml files
		def append_variants(file):
			filename = "./switches/{}_sw.pnml"
			stuff = codecs.open(filename.format(file),'r','utf8')
			sections.append(stuff.read())
			stuff.close()

		# Append header stuff which should always be first
		for i in levels:
			append_variants(i)

		# Write the content of 'sections' into a file and save it
		processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
		processed_pnml_file.write('\n'.join(sections))
		processed_pnml_file.close()

		print(building_name + " switches created using levels")

else:
	print("No " + building_name + " Switches Required")
