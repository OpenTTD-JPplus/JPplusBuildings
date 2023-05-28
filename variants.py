import pandas as pd
import codecs
import os
from buildings import buildings_dict as buildings_dict

buildings = list(buildings_dict.keys())

print("Running variants.py")

# CREATE THE VARIANTS FOR EACH BUILDING

for b in buildings:
    variants = list(buildings_dict[b]["variants"].keys())
    for v in variants:
        template = open("./src/houses/" + b + "/colours/all.pnml", "rt")
        current_variant = open("./src/houses/" + b + "/variants/" + v +".pnml", "wt")
        for line in template:
            try:
                if buildings_dict[b]["shared_variant_gfx"] == True and ("spritelayout" in line or "sprlay_" in line or "FEAT_HOUSES" in line):
                    current_variant.write(line.replace('_v_', str('_' + v +'_')))
                else:
                    current_variant.write(line.replace('_v_', str('_'))) 
            except:
                if v == 'x':
                    current_variant.write(line.replace('_v_', str('_')))                      
                else:
                    current_variant.write(line.replace('_v_', str('_' + v +'_')))
            
        template.close()
        current_variant.close()

        search_text_x = "_xoff_"
        search_text_y = "_yoff_"
        search_text_hide_sprite = "_hide_"
        search_text_construction_state = "_construction_state_"
        xoff = buildings_dict[b]["variants"][v]["xoffset"]
        yoff = buildings_dict[b]["variants"][v]["yoffset"]
        with open(r'./src/houses/' + b + '/variants/' + v +'.pnml', 'r') as file:
            data = file.read()
            # Offsets
            data = data.replace(search_text_x, xoff)
            data = data.replace(search_text_y, yoff)
            # Hide Sprites
            try: 
                hide_sprite = buildings_dict[b]["variants"][v]["hide_sprite"]
            except:    
                data = data.replace(search_text_hide_sprite, "0")
            else:
                data = data.replace(search_text_hide_sprite, hide_sprite)
            # Construction States
            try:
                construction_state = buildings_dict[b]["variants"][v]["construction_state"]
            except:
                data = data.replace(search_text_construction_state, "construction_state")
            else:
                data = data.replace(search_text_construction_state, construction_state)

        with open(r'./src/houses/' + b + '/variants/' + v+ '.pnml', 'w') as file:
            file.write(data)
        
        with open(r'./src/houses/' + b + '/variants/' + v + '.pnml', 'w') as file:		    
            file.write(data)
		    #get list of lines
        a_file = open(r'./src/houses/' + b + '/variants/' + v +'.pnml', 'r')	    
        lines = a_file.readlines()	    
        a_file.close()	    
        new_file = open(r'./src/houses/' + b+ '/variants/' + v + '.pnml', 'w')	    
        for line in lines:

		    #delete line matching string
            if line.find('xoffset: 0;') == -1:			      
                new_file.write(line)
	   
        new_file.close()

        a_file = open(r'./src/houses/' + b + '/variants/' + v +'.pnml', 'r')	    
        lines = a_file.readlines()	    
        a_file.close()	    
        new_file = open(r'./src/houses/' + b + '/variants/' + v + '.pnml', 'w')	    
        for line in lines:

		    #delete line matching string
            if line.find('yoffset: 0;') == -1:			      
                new_file.write(line)
	   
        new_file.close()

        a_file = open(r'./src/houses/' + b + '/variants/' + v +'.pnml', 'r')	    
        lines = a_file.readlines()	    
        a_file.close()	    
        new_file = open(r'./src/houses/' + b + '/variants/' + v + '.pnml', 'w')	    
        for line in lines:

		    #delete line matching string
            if line.find('hide_sprite: 0;') == -1:			      
                new_file.write(line)
	   
        new_file.close()

# COMBINE THE VARIANTS INTO AN 'ALL' FILE

# Cycle through each building and combine each of it's variants
m = 0
for b in buildings:
    sections = []
    variants = list(buildings_dict[buildings[m]]["variants"].keys())
    n = 0
    for v in variants:
        variants_pnml_path = "src/houses/" + buildings[m] + "/variants/all.pnml"
        filename = "src/houses/" + buildings[m] + "/variants/" + variants[n] + ".pnml"
        stuff = codecs.open(filename.format(v),'r','utf8')
        sections.append(stuff.read())
        stuff.close()
        n = n + 1
        processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
        processed_pnml_file.write('\n'.join(sections))
        processed_pnml_file.close()
    m = m+1
