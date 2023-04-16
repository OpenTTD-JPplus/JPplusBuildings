
# Mori

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
"black":		"11"
}

building_name = "mori"
colours = ["white", "grey", "mauve", "brown1", "brown2", "dark_green", "peach", "light_blue", "dark_blue"]
levels = ["3L", "4L", "5L", "6L"]
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

variant_names = list(variants.keys())

# 1) Create the variants	
# 2) Merge the variants 	
# 3) Create the levels		

# 1) CREATE THE DIRECTION / VARIANTS

import codecs

n = 0
for i in variants:
	switch_template = open("./template_rs.pnml", "rt")
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

n = 0
for i in levels:
	level_template = open("./switches/combined_variants.pnml", "rt")
	current_level = open("./switches/" + levels[n] +".pnml", "wt")
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
    filename = "./switches/{}.pnml"
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

print("random switches created")