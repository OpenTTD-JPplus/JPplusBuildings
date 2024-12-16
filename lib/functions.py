from buildings import buildings_dict as buildings
from lib import dictionaries, lists
import pandas as pd
import json, copy, itertools, codecs, os, shutil

def CreateRecolourPnml():
    colour_remaps = dictionaries.ColourRemapsDict()
    palette = dictionaries.PaletteDict()
    from lib.dictionaries import recolour_codes as recolour_codes

    # Create Recolour.pnml file
    website1 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Recolour_sprites'
    website2 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Builtin_functions'
    
    with open('src/recolour.pnml', 'w') as f:
        f.write(website1)
        f.write('\n\n' + website2 + '\n\n')
        f.write('recolour_remap = reserve_sprites(' + str(len(colour_remaps)) + ');\n\n')
        f.write('replace(recolour_remap) {\n')
        f.close()
    for c in colour_remaps:
        with open('src/recolour.pnml', 'a') as f:
            f.write('\n// ' + c + " +" + str(colour_remaps[c]))
            f.write('\n\trecolour_sprite {')
            for r in recolour_codes:
                f.write('\n\t\t' + recolour_codes[r] + str(palette[r][c]) + ';')
            f.write("\n\t}")
            f.close()
    with open('src/recolour.pnml', 'a') as f:
        f.write("\n}")
        f.close()

def CreateColourFiles():
    buildings_no_recolouring = lists.NoRecolouring()
    buildings_recolouring = lists.Recolouring()
    colour_all_dict = dictionaries.ColourAllDict()
    remap = dictionaries.ColourRemapsDict()

    # For buildings which require recolouring
    for b in buildings_recolouring:
        with open('./src/houses/' + b + '/colours/all.pnml', 'w') as f:
            f.write('\n// '+ b +' all colours\n')
            f.close()
        
        colours = colour_all_dict[b].keys()
        #colours = list(buildings[b]["colours"].keys())
        
        for c in colours:
            template = open("./src/templates/recolour_template.pnml", "rt")
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
            recolour_remap = str(remap[c])
            with open(r'./src/houses/' + b + '/colours/all.pnml', 'r') as file:
                data = file.read()
                # Override for ground sprites e.g. 'spr_ground_grass'
                try:
                    ground_sprite = buildings[b]["ground"]
                    data = data.replace(search_text_ground_snow, ground_sprite)
                    data = data.replace(search_text_ground, ground_sprite)            
                except:
                    pass
                # Override for building sprites
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

    # For buildings which DON'T require recolouring    
    for b in buildings_no_recolouring:
        with open('./src/houses/' + b + '/colours/all.pnml', 'w') as f:
            f.write('\n// '+ b +' all colours\n')
            f.close()

        template = open("./src/templates/norecolour_template.pnml", "rt")
        current_colour = open('./src/houses/' + b + '/colours/all.pnml', "a")
        for line in template:
            current_colour.write(line.replace('_clr_', str('_')))
        template.close()
        current_colour.close()

        search_text_ground = "spr_building_name_v_ground"
        search_text_ground_snow = "spr_building_name_v_ground_snow"
        search_text_building = "spr_building_name_v_xL_norm"
        search_text_building_snow = "spr_building_name_v_xL_snow"
        search_text_building_name = "building_name"
        with open(r'./src/houses/' + b + '/colours/all.pnml', 'r') as file:
            data = file.read()
            # Override for ground sprites e.g. 'spr_ground_grass'
            try:
                ground_sprite = buildings[b]["ground"]
                data = data.replace(search_text_ground_snow, ground_sprite)
                data = data.replace(search_text_ground, ground_sprite)            
            except:
                pass
            # Override for building sprites
            try:
                building_sprite = buildings[b]["building"]
                data = data.replace(search_text_building_snow, building_sprite + "_snow")
                data = data.replace(search_text_building, building_sprite + "_norm")  
            except:
                pass
            data = data.replace(search_text_building_name, b)
        with open(r'./src/houses/' + b + '/colours/all.pnml', 'w') as file:
            file.write(data)

def CreateVariantFiles():
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
    # Import various dictionaries and lists
    buildings_no_recolouring = lists.NoRecolouring()
    buildings_recolouring = lists.Recolouring()
    random_bits_all_range = dictionaries.RandomBitsAllRange()
    random_bits_old_range = dictionaries.RandomBitsOldRange()
    random_bits_total_all_dict = dictionaries.RandomBitsTotalAllDict()
    random_bits_total_old_dict = dictionaries.RandomBitsTotalOldDict()
    colour_all_dict = dictionaries.ColourAllDict()
    colour_old_dict = dictionaries.ColourOldDict()
    old_colour_buildings = lists.HasOldColours()

    # Add the lines for each colour option and it's random bit allocation
    for b in buildings_recolouring:
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
                if b not in old_colour_buildings and v == 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 1 \n")
                elif b not in old_colour_buildings and v != 'x' and (h == 'k' or h == 'c'):
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_" + v + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 2\n")   
                elif b not in old_colour_buildings and v != 'x' and h != "k":
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 3\n")  
                #Old Colours will come latter
                elif b in old_colour_buildings and v == 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_modern, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 4\n")
                elif b in old_colour_buildings and v != 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_modern, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 5\n")
                else:
                    print("// Ref 6 - " + b + " not allocated to an option")
                
                f.close()
                levels = list(buildings[b]["heights"].values())[n]
                n = n + 1
                m = 0
                for l in levels:
                    colours = colour_all_dict[b].keys()
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
    for b in old_colour_buildings:
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
                    old_colours = list(colour_old_dict[b].keys())
                    for c in old_colours:
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
    for b in buildings_recolouring:
        if b not in old_colour_buildings:
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
        elif variants == ['a', 'b', 'e', 'n', 's', 'w']:    
            for h in heights:
                with open(r'./src/templates/spritedirections_abensw.pnml', 'r') as file:    
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
        elif variants == ['a', 'b'] or variants == ['a', 'b', 'c'] or variants == ['a', 'b', 's'] or variants == ['a', 'b', 'e', 'n', 's', 'w']:
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
        elif variants == ['a', 'b'] or variants == ['a', 'b', 'c'] or variants == ['a', 'b', 's'] or variants == ['a', 'b', 'e', 'n', 's', 'w']:
            for h in heights:    
                file_path = "src/houses/" + b + "/switches/" + h + ".pnml"
                try:
                    os.remove(file_path)
                except OSError as e:
                    print("Error: %s : %s" % (file_path, e.strerror))
        else:
            print(b + " has an unrecognised variant #3")

def PnmlCombiner():
    
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
            pass
        # Directional switches
        if variants == ['x'] or variants == ['north', 'east', 'west', 'south'] or variants == ['north', 'east'] or variants == ['north', 'west']:
            pass
        elif variants == ['a', 'b'] or variants == ['a', 'b', 'c'] or variants == ['a', 'b', 's'] or variants == ['a', 'b', 'e', 'n', 's', 'w']: 
            f.write('\n#include "src/houses/' + b +'/switches/direction_switches.pnml"')
        else:
            print(b + " has an unrecognised variant #4 pnml_combiner.py")
        f.close()

def CreateItems():

    all_buildings = dictionaries.ItemsTab()
    active_buildings = lists.ActiveBuildings()
    active_building_items = lists.ActiveBuildingItems()
    parameter_buildings = lists.ParameterBuildings()

    f = open("./src/houses.pnml", "w")
    f.write('\n// House pnml files\n')
    f.close()
    for b in active_buildings:
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

    for b in all_buildings:
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
            data = data.replace('_protection_', str(all_buildings[b]["protection"]))

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
    for b in active_building_items:
        append_variants(b)

    # Write the content of 'sections' into a file and save it
    processed_pnml_file = codecs.open(items_pnml_path,'w','utf8')
    processed_pnml_file.write('\n'.join(sections))
    processed_pnml_file.close()

    print("Items created")
