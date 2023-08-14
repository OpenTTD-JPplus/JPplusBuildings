import pandas as pd
import json
import codecs

def ImportColoursTab():
    print("\tRunning ImportColoursTab")
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