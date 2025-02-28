from buildings import buildings_dict as buildings
from lib import dictionaries
import pandas as pd
import json, copy, itertools, codecs, os, shutil

def ExportToJSON(dictionary, target_file):
    with open(target_file, 'w') as fp:
        json.dump(dictionary, fp, indent=4)

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

def non_zero_value(item):
    k, v = item
    return v != 0

def non_nan_value(item):
    k, v = item
    return v != 'nan'

def NameColumnColour(x):
    if 'old_colours' in x['name']:
        return 'old'
    else:
        return 'all'

recolour_codes  = {
        'palette01': '0xC6: 0x', 
        'palette02': '0xC7: 0x', 
        'palette03': '0xC8: 0x', 
        'palette04': '0xC9: 0x', 
        'palette05': '0xCA: 0x', 
        'palette06': '0xCB: 0x', 
        'palette07': '0xCC: 0x', 
        'palette08': '0xCD: 0x',
        'palette09': '0x50: 0x', 
        'palette10': '0x51: 0x', 
        'palette11': '0x52: 0x', 
        'palette12': '0x53: 0x', 
        'palette13': '0x54: 0x', 
        'palette14': '0x55: 0x', 
        'palette15': '0x56: 0x', 
        'palette16': '0x57: 0x', 
        }

palette_numbers = list(recolour_codes.keys())

def CreateRemapJSON():
    # convert excel spreadsheet into dataframe
    df1 = pd.read_excel('docs/buildings.ods','colours')
    df2 = df1[df1['name'].str.contains('remap|palette', case=False)]
    df3 = df2.set_index('name').transpose()

    all_columns = list(df3) # Creates list of all column headers
    palette_columns = [x for x in all_columns if "palette" in x]
    
    for p in palette_columns:
        df3[p] = df3[p].astype(str).str.zfill(2)

    # convert dataframe into dictionary
    raw_colour_profiles = df3.T.to_dict('dict')

    colour_profiles = {}
    for k, v in raw_colour_profiles.items():
        if isinstance(v, dict):
            colour_profiles[k] = dict(filter(non_nan_value, v.items()))
        else:
            colour_profiles[k] = v

    ExportToJSON(colour_profiles, 'lib/recolour.json')

def CreateBuildingPalettes():
    # convert excel spreadsheet into dataframe
    df_pal = pd.read_excel('docs/buildings.ods','colours')
    df_pal = df_pal[~df_pal['name'].isin(palette_numbers)]
    df_pal = df_pal[~df_pal['name'].isin(['remap', 'include'])]
    df_pal['colours'] = df_pal.apply(NameColumnColour, axis=1)
    df_pal['name'] = df_pal.name.str.removesuffix('_all_colours')
    df_pal['name'] = df_pal.name.str.removesuffix('_old_colours')

    building_palettes = df_pal.groupby('name').apply(lambda x: x.set_index('colours').to_dict(orient='index')).to_dict()
    
    # delete 0 probabilities and unnecessary names
    for b in building_palettes:
        # all colours
        del building_palettes[b]["all"]["name"]
        all_colours = list(building_palettes[b]["all"].keys())
        for c in all_colours:
            if building_palettes[b]["all"][c] == 0:
                del building_palettes[b]["all"][c]
        # old colours
        try:
            del building_palettes[b]["old"]["name"]
            old_colours = list(building_palettes[b]["old"].keys())
            for c in old_colours:
                if building_palettes[b]["old"][c] == 0:
                    del building_palettes[b]["old"][c]
        except:
            pass



    ExportToJSON(building_palettes, 'lib/building_palettes.json')

def CreateRecolourPnml():
    recolour_json = LoadJSON('lib/recolour.json')

    # Create Recolour.pnml file
    website1 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Recolour_sprites'
    website2 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Builtin_functions'

    
    with open('src/recolour.pnml', 'w') as f:
        f.write(website1)
        f.write('\n\n' + website2 + '\n\n')
        f.write('recolour_remap = reserve_sprites(' + str(len(recolour_json)) + ');\n\n')
        f.write('replace(recolour_remap) {\n')
        f.close()
    for c in recolour_json:
        replacements = list(recolour_json[c].keys())
        replacements.remove('remap')
        with open('src/recolour.pnml', 'a') as f:
            f.write('\n// ' + c + " +" + str(recolour_json[c]["remap"]))
            f.write('\n\trecolour_sprite {')
            for r in replacements:
                f.write('\n\t\t' + recolour_codes[r] + str(recolour_json[c][r]) + ';')
            f.write("\n\t}")
            f.close()
    with open('src/recolour.pnml', 'a') as f:
        f.write("\n}")
        f.close()

def CreateItemJSON():
    # convert excel spreadsheet into dataframe
    df_items = pd.read_excel('docs/buildings.ods','items')
    df_items[['flags', 'building_flags']] = df_items[['flags', 'building_flags']].fillna(0)

    items = df_items.set_index('name').T.to_dict('dict')
    
    ExportToJSON(items, 'lib/items.json')

def CheckColourWeightingPresent():
    items = LoadJSON('lib/items.json')
    buildings_recolouring_all = {items[x]["folder"] for x in items if items[x]["recolour"] == True }
    buildings_recolouring_old = {items[x]["folder"] for x in items if items[x]["old_colours"] == True }

    building_palettes = LoadJSON('lib/building_palettes.json')
    building_palettes_all = [x for x in building_palettes if 'all' in building_palettes[x].keys()]
    building_palettes_old = [x for x in building_palettes if 'old' in building_palettes[x].keys()]
   
    missing_building_palettes_all = [x for x in buildings_recolouring_all if x not in building_palettes_all]
    missing_building_palettes_old = [x for x in buildings_recolouring_old if x not in building_palettes_old]

    if len(missing_building_palettes_all) > 0:
        print(missing_building_palettes_all)
        raise Exception("Missing building palette all")

    if len(missing_building_palettes_old) > 0:
        print(missing_building_palettes_old)
        raise Exception("Missing building palette old")

def CheckBuildingSchema():
    items = LoadJSON('lib/items.json')
    buildings = LoadJSON('lib/buildings.json')

    folders = {items[x]["folder"] for x in items}
    schema = [x for x in buildings]

    check = [x for x in folders if x not in buildings]

    if len(check) > 0:
        print(check)
        raise Exception("Building not in schema")

def CreateProbabilitiesJSON():
    items = LoadJSON('lib/items.json')
    buildings = LoadJSON('lib/buildings.json')
    building_palettes = LoadJSON('lib/building_palettes.json')

    #initial_dict = {k: v for d in [d1, d2] for k, v in d.items()}

    #print(initial_dict)

def NumHeights():
    schema = LoadJSON('lib/buildings.json')

    buildings = {x: schema[x]["heights"] for x in schema}
    for b in buildings:
        heights = list(buildings[b].keys())
        for h in heights:
            buildings[b][h] = len(buildings[b][h])
    print(buildings)

    

def CreateColourFiles():
    
    building_palettes = LoadJSON('lib/building_palettes.json')
    items = LoadJSON('lib/items.json')

    buildings_no_recolouring = {items[x]["folder"] for x in items if items[x]["recolour"] == False }
    buildings_recolouring = {items[x]["folder"] for x in items if items[x]["recolour"] == True }

    recolour = LoadJSON('lib/recolour.json')
    remap = {x: recolour[x]["remap"] for x in recolour}

    # For buildings which require recolouring
    for b in buildings_recolouring:
        with open('./src/houses/' + b + '/colours/all.pnml', 'w') as f:
            f.write('\n// '+ b +' all colours\n')
            f.close()
        
        colours = building_palettes[b]["all"].keys()
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
    building_palettes = LoadJSON('lib/building_palettes.json')
    items = LoadJSON('lib/items.json')

    buildings_no_recolouring = {items[x]["folder"] for x in items if items[x]["recolour"] == False }
    buildings_recolouring = {items[x]["folder"] for x in items if items[x]["recolour"] == True }
    old_colour_buildings = {items[x]["folder"] for x in items if items[x]["old_colours"] == True }

    # Import various dictionaries and lists
    random_bits_all_range = dictionaries.RandomBitsAllRange()
    random_bits_old_range = dictionaries.RandomBitsOldRange()
    random_bits_total_all_dict = dictionaries.RandomBitsTotalAllDict()
    random_bits_total_old_dict = dictionaries.RandomBitsTotalOldDict()

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
                    colours = building_palettes[b]["all"].keys()
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
                    old_colours = list(building_palettes[b]["old"].keys())
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

def CreateNameSwitches():
    items = LoadJSON('lib/items.json')

    name_switch_buildings = {items[x]["folder"] for x in items if items[x]["name_switch"] != 'none' }

    random_bits_total_all_dict = dictionaries.RandomBitsTotalAllDict()

    for b in name_switch_buildings:
        f = open("./src/houses/" + b + "/switches/name_switches.pnml", "w")
        f.write("\n// " + b + " ALL Names\n")
        f.close()
        variants = list(buildings[b]["levels"])
        f = open("./src/houses/" + b + "/switches/name_switches.pnml", "a")
        f.write("\nswitch (FEAT_HOUSES, SELF, name_" + b + ", random_bits % " + str(random_bits_total_all_dict[b] * len(variants)) + " ) { // Ref functions.CreateNameSwitches() \n")
        m = 0
        for v in variants:
            # When there are ranges
            if random_bits_total_all_dict[b] > 1:
                f.write("\t" + str(m) + ".." + str(m + random_bits_total_all_dict[b] - 1) + ": \treturn string(" + str(buildings[b]["names"][v]) + ");\n")
                m = m + random_bits_total_all_dict[b]
            # When there is single numbers
            else:
                f.write("\t" + str(m) + ": \treturn string(" + str(buildings[b]["names"][v]) + ");\n")
                m = m + 1
        f.write("}\n")
        f.close()

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
        # Name switches
        if os.path.exists('./src/houses/' + b +'/switches/name_switches.pnml'):
            f.write('\n#include "src/houses/' + b +'/switches/name_switches.pnml"')
        else:
            pass
        f.close()

def CreateItems():

    items = LoadJSON('lib/items.json')

    active_building_names = [x for x in items if items[x]["include"] == True]
    active_building_folders = {items[x]["folder"] for x in items if items[x]["include"] == True}
    parameter_buildings = [x for x in items if items[x]["param_top"] != 'none']

    all_buildings = dictionaries.ItemsTab()

    f = open("./src/houses.pnml", "w")
    f.write('\n// House pnml files\n')
    f.close()
    for b in active_building_folders:
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
            data = data.replace('_nameswitch_', str(all_buildings[b]["name_switch"]))

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
    for b in active_building_names:
        append_variants(b)

    # Write the content of 'sections' into a file and save it
    processed_pnml_file = codecs.open(items_pnml_path,'w','utf8')
    processed_pnml_file.write('\n'.join(sections))
    processed_pnml_file.close()

    print("Items created")
