import pandas as pd
import codecs

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

buildings = {
	"fukuda_m" : {
		"height1" : "6L",
	}, 
	"l" : {
		"height1" : "8L",
	}
}

# convert into dataframe
df2 = pd.read_excel("docs/buildings.xlsx", sheet_name = 'colours')

# convert into dictionary
building_colours_dict = df2.to_dict()
name = list(building_colours_dict["name"].values())

print(name)

# 1) CREATE THE COLOURS

'''
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
'''