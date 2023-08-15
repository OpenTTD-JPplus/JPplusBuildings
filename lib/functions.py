import pandas as pd
import json
import copy
import itertools
import codecs
import os, shutil

def ImportColoursTab():
    # convert excel spreadsheet into dataframe
    df1 = pd.read_excel('docs/buildings.xlsx','colours')
    # convert dataframe into dictionary
    raw_colour_profiles = df1.set_index('name').T.to_dict('dict')

    # REMAPS - get colours with their remap number
    colours = raw_colour_profiles['remap']

    # REMAPS - create remap.py
    with open('lib/remap.py', 'w') as f:
        f.write("\n# Remap\n")
        f.write("\nremap = {")
        f.close()
    for c in colours:
        with open('lib/remap.py', 'a') as f:
            f.write('\n"' + c + '": "' + str(colours[c]) + '",')
            f.close()
    with open('lib/remap.py', 'a') as f:
        f.write("\n}")
        f.close()

    # PALETTE - create palette dictionary
    
    recolour_codes  = {
        'palette01': '0xC6: 0x', 
        'palette02': '0xC7: 0x', 
        'palette03': '0xC8: 0x', 
        'palette04': '0xC9: 0x', 
        'palette05': '0xCA: 0x', 
        'palette06': '0xCB: 0x', 
        'palette07': '0xCC: 0x', 
        'palette08': '0xCD: 0x', 
        }

    keys = list(recolour_codes.keys())

    palette = raw_colour_profiles.copy()
    for p in raw_colour_profiles:
        if p not in recolour_codes:
            palette.pop(p, None)
        else:
            pass

    # Convert colour codes to two digit strings
    for p in palette:
        for c in colours:
            if len(str(palette[p][c])) == 2:
                palette[p][c] = str(palette[p][c])
            else:
                palette[p][c] = str("0" + str(palette[p][c]))

    # Create Recolour.pnml file
    website1 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Recolour_sprites'
    website2 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Builtin_functions'
    
    with open('src/recolour.pnml', 'w') as f:
        f.write(website1)
        f.write('\n\n' + website2 + '\n\n')
        f.write('recolour_remap = reserve_sprites(' + str(len(colours)) + ');\n\n')
        f.write('replace(recolour_remap) {\n')
        f.close()
    for c in colours:
        with open('src/recolour.pnml', 'a') as f:
            f.write('\n// ' + c + " +" + str(colours[c]))
            f.write('\n\trecolour_sprite {')
            for r in recolour_codes:
                f.write('\n\t\t' + recolour_codes[r] + str(palette[r][c]) + ';')
            f.write("\n\t}")
            f.close()
    with open('src/recolour.pnml', 'a') as f:
        f.write("\n}")
        f.close()
            
    # BUILDINGS
    colour_profiles = raw_colour_profiles.copy()
    colour_profiles.pop('remap', None)
    for key in keys:
        colour_profiles.pop(key, None)
    
    # Remove colours with nil probability
    for b in colour_profiles:
        colour_profiles[b] = {keys:values for keys, values in colour_profiles[b].items() if values != 0}

   # create colour profile dictionaries
    with open('lib/colourprofiles.py', 'w') as f:
        f.write("\n# Colour Profiles\n")
        f.close()
    for b in colour_profiles:
        with open('lib/colourprofiles.py', 'a') as f:
            f.write("\n")
            f.write(str(b) + " = ")
            f.write(json.dumps(colour_profiles[b]))
            f.write("\n")
            f.close()

    file1 = open('lib/colourprofiles.py', 'r')
    file2 = open('buildings.py', 'r')

    # Read the contents of the text files
    content1 = file1.read()
    content2 = file2.read()

    # Close the source text files
    file1.close()
    file2.close()

    # Open the destination file
    destination_file = open('lib/buildings_and_colours.py', 'w')

    # Write the concatenated content to the destination file
    destination_file.write(content1 + content2)
    # Close the destination file
    destination_file.close()

def CreateColourFiles():
    from lib.buildings_and_colours import buildings_dict as buildings
    from lib.remap import remap as remap

    for b in buildings:
        with open('./src/houses/' + b + '/colours/all.pnml', 'w') as f:
            f.write('\n// '+ b +' all colours\n')
            f.close()
        colours = list(buildings[b]["colours"].keys())
        
        for c in colours:
            template = open("./src/templates/colour_template.pnml", "rt")
            current_colour = open('./src/houses/' + b + '/colours/all.pnml', "a")
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
            recolour_remap = remap[c]
            with open(r'./src/houses/' + b + '/colours/all.pnml', 'r') as file:
                data = file.read()
                try:
                    ground_sprite = buildings[b]["ground"]
                    data = data.replace(search_text_ground_snow, ground_sprite)
                    data = data.replace(search_text_ground, ground_sprite)            
                except:
                    pass
                try:
                    building_sprite = buildings[b]["building"]
                    data = data.replace(search_text_building_snow, building_sprite + "_snow")
                    data = data.replace(search_text_building, building_sprite + "_norm")  
                except:
                    pass
                data = data.replace(search_text_remap, recolour_remap)
                data = data.replace(search_text_building_name, b)
            with open(r'./src/houses/' + b + '/colours/all.pnml', 'w') as file:
                file.write(data)

def CreateVariantFiles():
    from lib.buildings_and_colours import buildings_dict as buildings

    for b in buildings:
        variants = list(buildings[b]["variants"].keys())
        for v in variants:
            template = open("./src/houses/" + b + "/colours/all.pnml", "rt")
            current_variant = open("./src/houses/" + b + "/variants/" + v +".pnml", "wt")
            for line in template:
                try:
                    if buildings[b]["shared_variant_gfx"] == True and ("spritelayout" in line or "sprlay_" in line or "FEAT_HOUSES" in line):
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
            xoff = buildings[b]["variants"][v]["xoffset"]
            yoff = buildings[b]["variants"][v]["yoffset"]
            with open(r'./src/houses/' + b + '/variants/' + v +'.pnml', 'r') as file:
                data = file.read()
                # Offsets
                data = data.replace(search_text_x, xoff)
                data = data.replace(search_text_y, yoff)
                # Hide Sprites
                try: 
                    hide_sprite = buildings[b]["variants"][v]["hide_sprite"]
                except:    
                    data = data.replace(search_text_hide_sprite, "0")
                else:
                    data = data.replace(search_text_hide_sprite, hide_sprite)
                # Construction States
                try:
                    construction_state = buildings[b]["variants"][v]["construction_state"]
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
    for b in buildings:
        sections = []
        variants = list(buildings[b]["variants"].keys())
        for v in variants:
            variants_pnml_path = "src/houses/" + b + "/variants/all.pnml"
            filename = "src/houses/" + b + "/variants/" + v + ".pnml"
            stuff = codecs.open(filename.format(v),'r','utf8')
            sections.append(stuff.read())
            stuff.close()
            processed_pnml_file = codecs.open(variants_pnml_path,'w','utf8')
            processed_pnml_file.write('\n'.join(sections))
            processed_pnml_file.close()

def CreateLevelsFiles():
    from lib.buildings_and_colours import buildings_dict as buildings

    for b in buildings:
        levels_pnml = open("src/houses/" + b + "/levels/all.pnml", "wt")
        levels_pnml.write("\n// " + b + " levels\n")
        levels_pnml.close()
        levels = list(buildings[b]["levels"])
        for l in levels:
            template = open("./src/houses/" + b + "/variants/all.pnml", "rt")
            current_level = open("./src/houses/" + b + "/levels/all.pnml", "a")
            for line in template:
                if l == 'sky' or l == "x":
                    current_level.write(line.replace('_xL_', str('_')))
                else:
                    current_level.write(line.replace('_xL_', str('_' + l +'_')))
            template.close()
            current_level.close()

def CreateColourSwitches():
    from lib.buildings_and_colours import buildings_dict as buildings

    colour_dict = {}
    colour_weightings_all_dict = {}
    colour_weightings_old_dict = {}
    for b in buildings:
        colours = list(buildings[b]["colours"].keys())
        for c in colours:
            colour_dict[b] = buildings[b]["colours"]
            colour_weightings_all_dict[b] = list(buildings[b]["colours"].values())
            if buildings[b]["old_colours"] == False:
                colour_weightings_old_dict[b] = False
            else:
                colour_weightings_old_dict[b] = list(buildings[b]["old_colours"].values())

    # Create dictionary showing what levels are available per height
    heights_dict = {}
    for b in buildings:
        heights = list(buildings[b]["heights"])
        for h in heights:
            heights_dict[b] = (buildings[b]["heights"])

    # Create dictionary with number of levels per height
    num_heights_dict = copy.deepcopy(heights_dict)
    for b in buildings:
        heights = list(buildings[b]["heights"])
        for h in heights:
            num_heights_dict[b][h] = len(num_heights_dict[b][h]) # {'fukuda': {'m': 1, 'l': 1}, 'harada': {'m': 1, 'l': 1}, 'hayashi': {'s': 2, 'm': 2}, 'hirano': {'s': 2, 'm': 2}}

    # Map the colour weighting to each building and each height
    colour_weightings_all_levels_dict = copy.deepcopy(colour_weightings_all_dict)
    colour_weightings_old_levels_dict = copy.deepcopy(colour_weightings_old_dict)

    colours_all_weightings = copy.deepcopy(num_heights_dict)
    for b in buildings:
        heights = list(colours_all_weightings[b].keys())
        for h in heights:
            colours_all_weightings[b][h] = colour_weightings_all_levels_dict[b] * num_heights_dict[b][h] 

    colours_old_weightings = copy.deepcopy(num_heights_dict)
    for b in buildings:
        heights = list(colours_old_weightings[b].keys())
        for h in heights:
            if buildings[b]["old_colours"] == False:
                colours_old_weightings[b][h] = False
            else:
                colours_old_weightings[b][h] = colour_weightings_old_levels_dict[b] * num_heights_dict[b][h] 

    # Calculate the end point of the random bits
    end_point_all = copy.deepcopy(colours_all_weightings)
    end_point_old = copy.deepcopy(colours_old_weightings)
    for b in buildings:
        heights = list(colours_all_weightings[b].keys())
        for h in heights:
            end_point_all[b][h] = list(itertools.accumulate(colours_all_weightings[b][h]))
            end_point_all[b][h] = [x - 1 for x in end_point_all[b][h]]
            if buildings[b]["old_colours"] == False:
                end_point_old[b][h] = False
            else:
                end_point_old[b][h] = list(itertools.accumulate(colours_old_weightings[b][h]))
                end_point_old[b][h] = [x - 1 for x in end_point_old[b][h]]

    # Calculate the start point of the random bits
    start_point_all = copy.deepcopy(end_point_all)
    start_point_old = copy.deepcopy(end_point_old)
    for b in buildings:
        heights = list(start_point_all[b].keys())
        heights_old = list(start_point_old[b].keys())
        # For ALL colours
        for h in heights:
            bits = list(start_point_all[b][h])
            n = 0
            for g in bits:
                start_point_all[b][h][n] = end_point_all[b][h][n] - ( colours_all_weightings[b][h][n] - 1)
                n = n + 1
        # For OLD colours
        for i in heights_old:
            m = 0
            if buildings[b]["old_colours"] == False:
                start_point_old[b][i] = False
                m = m + 1
            else:
                bits_old = list(start_point_old[b][i])
                for f in bits_old: 
                    start_point_old[b][i][m] = end_point_old[b][i][m] - ( colours_old_weightings[b][i][m] - 1)
                    m = m + 1

    # Calculate the random bit range
    random_bits_all_range = copy.deepcopy(end_point_all)
    random_bits_old_range = copy.deepcopy(end_point_old)
    for b in buildings:
        heights = list(random_bits_all_range[b].keys())
        heights_old = list(random_bits_old_range[b].keys())
        # For ALL colours
        for h in heights:
            bits = list(random_bits_all_range[b][h])
            n = 0
            for g in bits:
                if start_point_all[b][h][n] == end_point_all[b][h][n]:
                    random_bits_all_range[b][h][n] = str(start_point_all[b][h][n])
                else:
                    random_bits_all_range[b][h][n] = str(start_point_all[b][h][n]) + ".." + str(end_point_all[b][h][n])
                n = n + 1
        # For OLD colours
        for i in heights_old:
            m = 0
            if buildings[b]["old_colours"] == False:
                random_bits_old_range[b][i] = False
                m = m + 1
            else:
                bits_old = list(start_point_old[b][i])
                for f in bits_old: 
                    if start_point_old[b][h][m] == end_point_old[b][h][m]:
                        random_bits_old_range[b][i][m] = str(start_point_old[b][i][m])
                    else:
                        random_bits_old_range[b][i][m] = str(start_point_old[b][i][m]) + ".." + str(end_point_old[b][i][m])
                    m = m + 1

    # Calculate the random bits totals - adj for number of levels is made later
    random_bits_total_all_dict = {}
    for b in buildings:
        random_bits_total_all_dict[b] = sum(buildings[b]["colours"].values())

    random_bits_total_old_dict = {}
    for b in buildings:
        if buildings[b]["old_colours"] == False:
            random_bits_total_old_dict[b] = False
        else:
            random_bits_total_old_dict[b] = sum(buildings[b]["old_colours"].values())


    # Add the lines for each colour option and it's random bit allocation
    for b in buildings:
        # Create an initial file
        f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "w")
        f.write("\n// " + b + " ALL colours\n")
        f.close()
        variants = list(buildings[b]["variants"])
        for v in variants:
            heights = list(buildings[b]["heights"]) # 's', 'm', 'l' etc
            n = 0
            for h in heights:
                num_heights = len(buildings[b]["heights"][h])
                # Add the switch line and update details
                f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                # Modern Colours only
                if buildings[b]["old_colours"] == False and v == 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 1 \n")
                elif buildings[b]["old_colours"] == False and v != 'x' and (h == 'k' or h == 'c'):
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_" + v + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 2\n")   
                elif buildings[b]["old_colours"] == False and v != 'x' and h != "k":
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 3\n")  
                #Old Colours will come latter
                elif buildings[b]["old_colours"] != False and v == 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_modern, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 4\n")
                elif buildings[b]["old_colours"] != False and v != 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_modern, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 5\n")
                else:
                    print("// Ref 6 - " + b + " not allocated to an option")
                
                f.close()
                levels = list(buildings[b]["heights"].values())[n]
                n = n + 1
                m = 0
                for l in levels:
                    colours = list(buildings[b]["colours"].keys())
                    for c in colours:
                        # Add the colours lines
                        f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                        if v == 'x' and (l == 'sky' or l == 'x'):
                            f.write(str(random_bits_all_range[b][h][m]) + ": switch_" + b + "_" + c +"_snow;\n")
                        elif v == 'x' and l != 'sky':    
                            f.write(str(random_bits_all_range[b][h][m]) + ": switch_" + b + "_" + l + "_" + c +"_snow;\n")
                        elif v != 'x' and (l == 'sky' or l == 'x'):
                            f.write(str(random_bits_all_range[b][h][m]) + ": switch_" + b + "_" + v + "_" + c +"_snow;\n")
                        else:
                            f.write(str(random_bits_all_range[b][h][m]) + ": switch_" + b + "_" + v + "_" + l + "_" + c +"_snow;\n")
                        f.close()
                        m = m + 1
                # Add bracket at the bottom
                f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                f.write("}\n")
                f.close()

    # For buildings with old colour subsets, append those switches
    for b in buildings:
        if buildings[b]["old_colours"] == False:
            pass
        else:
            f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
            f.write("\n// " + b + " OLD colours\n")
            f.close()
            variants = list(buildings[b]["variants"])
            for v in variants:
                heights = list(buildings[b]["heights"])
                n = 0
                for h in heights:
                    num_heights = len(buildings[b]["heights"][h])
                    # Add the switch line and update details
                    f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                    if v == 'x':
                        f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_old, random_bits % " + str(random_bits_total_old_dict[b] * num_heights) + " ) {\n")
                    else:
                        f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_old, random_bits % " + str(random_bits_total_old_dict[b] * num_heights) + " ) {\n")
                    f.close()
                    levels = list(buildings[b]["heights"].values())[n]
                    n = n + 1
                    m = 0
                    for l in levels:
                        colours = list(buildings[b]["old_colours"].keys())
                        for c in colours:
                            # Add the colours lines
                            f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                            if v == 'x':
                                f.write(str(random_bits_old_range[b][h][m]) + ": switch_" + b + "_" + l + "_" + c +"_snow;\n")
                            else:
                                f.write(str(random_bits_old_range[b][h][m]) + ": switch_" + b + "_" + v + "_" + l + "_" + c +"_snow;\n")
                            f.close()
                            m = m + 1
                    # Add bracket at the bottom
                    f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                    f.write("}\n")
                    f.close()

    # Switch to pick between OLD and MODERN colours depending on year
    for b in buildings:
        if buildings[b]["old_colours"] == False:
            pass
        else:
            f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
            f.write("\n// " + b + " switch to choose between old and modern colours")
            variants = list(buildings[b]["variants"])
            for v in variants:
                heights = list(buildings[b]["heights"])
                n = 0
                for h in heights:
                    # Add the switch line and update details
                    f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                    if v == 'x':
                        f.write("\n\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_sprites, current_year - age) {")
                    else:
                        f.write("\n\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_sprites, current_year - age) {")
                    if v == 'x':
                        f.write("\n0.." + str(buildings[b]["end_of_old_era"]) + ": switch_" + b + "_" + h + "_old;")  
                    else:
                        f.write("\n0.." + str(buildings[b]["end_of_old_era"]) + ": switch_" + b + "_" + v + "_" + h + "_old;")               
                    if v == 'x':
                        f.write("\nswitch_" + b + "_" + h + "_modern;") 
                    else:
                        f.write("\nswitch_" + b + "_" + v + "_" + h + "_modern;") 
                    # Add bracket at the bottom
                    f.write("\n}")
                    f.close()
                    n = n + 1

def CreateDirectionSwitches():
    from lib.buildings_and_colours import buildings_dict as buildings
    # Create a spritedirection file for relevant buildings
    for b in buildings:
        heights = list(buildings[b]["heights"])
        variants = list(buildings[b]["variants"].keys())
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
        elif variants == ['a', 'b', 's']:    
            for h in heights:
                with open(r'./src/templates/spritedirections_abs.pnml', 'r') as file:    
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
        heights = list(buildings[b]["heights"])
        variants = list(buildings[b]["variants"].keys())
        if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
            pass
        elif variants == ['a', 'b'] or variants == ['a', 'b', 'c'] or variants == ['a', 'b', 's']: 
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
        heights = list(buildings[b]["heights"])
        variants = list(buildings[b]["variants"].keys())
        if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
            pass
        elif variants == ['a', 'b'] or variants == ['a', 'b', 'c'] or variants == ['a', 'b', 's']: 
            for h in heights:    
                file_path = "src/houses/" + b + "/switches/" + h + ".pnml"
                try:
                    os.remove(file_path)
                except OSError as e:
                    print("Error: %s : %s" % (file_path, e.strerror))
        else:
            print(b + " has an unrecognised variant #3")

def PnmlCombiner():
    from lib.buildings_and_colours import buildings_dict as buildings

    folders = ["levels", "colours", "variants"]

    manual_gfx = copy.deepcopy(buildings)
    manual_switches = copy.deepcopy(buildings)
    for b in buildings:
        try:
            buildings[b]["manual_gfx"] == True
        except:
            manual_gfx.pop(b)
        try:
            buildings[b]["manual_switches"] == True
        except:
            manual_switches.pop(b)

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
        variants = list(buildings[b]["variants"].keys())
        f = open("./src/houses/" + b + "/" + b +".pnml", "w")
        f.write("\n// " + b + "\n")
        # Sprites
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
        elif variants == ['a', 'b'] or variants == ['a', 'b', 'c'] or variants == ['a', 'b', 's']: 
            f.write('\n#include "src/houses/' + b +'/switches/direction_switches.pnml"')
        else:
            print(b + " has an unrecognised variant #4 pnml_combiner.py")
        f.close()

def CreateItems():

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
