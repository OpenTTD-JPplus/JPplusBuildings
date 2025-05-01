#from buildings import buildings_dict as buildings
from lib import dictionaries
import pandas as pd
import json, copy, itertools, codecs, os, shutil, ast
from itertools import accumulate

# Define common file paths
buildingsJSON = 'lib/new_buildings.json'
recolourJSON = 'lib/recolour.json'

def ExportToJSON(dictionary, target_file):
    with open(target_file, 'w') as fp:
        json.dump(dictionary, fp, indent=4)

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

buildings = LoadJSON(buildingsJSON)

def non_zero_value(item):
    k, v = item
    return v != 0

def non_nan_value(item):
    k, v = item
    return v != 'nan'

def CleanNones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [CleanNones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: CleanNones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value

def NameColumnColour(x):
    if 'old_colours' in x['name']:
        return 'old'
    else:
        return 'all'

def GraphicsDefault(x):
    if x['tile_size'] != '1X1':
        return 'none'
    else:
        if x['recolour'] == True:
            if x['height'] == 'skyscraper':
                return str(x['name'] + '_c')
            elif x['height'] == 'landmark':
                return str(x['name'] + '_k')
            elif x['height'] == 'house':
                return str(x['name'] + '_h')
            else:
                return str(x['name'])
        else:
            return str(x['name'])

def GraphicsNorth(x):
    if x['tile_size'] == '1X1':
        return 'none'
    else:
        if x['recolour'] == True:
            if x['height'] == 'skyscraper':
                return str(x['name'] + '_c_north')
            elif x['height'] == 'landmark':
                return str(x['name'] + '_k_north')
            elif x['height'] == 'house':
                return str(x['name'] + '_h_north')
            else:
                return str(x['name'] + '_north')
        else:
            return str(x['name'] + '_north')

def GraphicsEast(x):
    if x['tile_size'] == '1X1' or x['tile_size'] == '2X1':
        return 'none'
    else:
        if x['recolour'] == True:
            if x['height'] == 'skyscraper':
                return str(x['name'] + '_c_east')
            elif x['height'] == 'landmark':
                return str(x['name'] + '_k_east')
            elif x['height'] == 'house':
                return str(x['name'] + '_h_east')
            else:
                return str(x['name'] + '_east')
        else:
            return str(x['name'] + '_east')

def GraphicsWest(x):
    if x['tile_size'] == '1X1' or x['tile_size'] == '1X2':
        return 'none'
    else:
        if x['recolour'] == True:
            if x['height'] == 'skyscraper':
                return str(x['name'] + '_c_west')
            elif x['height'] == 'landmark':
                return str(x['name'] + '_k_west')
            elif x['height'] == 'house':
                return str(x['name'] + '_h_west')
            else:
                return str(x['name'] + '_west')
        else:
            return str(x['name'] + '_west')

def GraphicsSouth(x):
    if x['tile_size'] != '2X2':
        return 'none'
    else:
        if x['recolour'] == True:
            if x['height'] == 'skyscraper':
                return str(x['name'] + '_c_south')
            elif x['height'] == 'landmark':
                return str(x['name'] + '_k_south')
            elif x['height'] == 'house':
                return str(x['name'] + '_h_south')
            else:
                return str(x['name'] + '_south')
        else:
            return str(x['name'] + '_south')

def GraphicDefault(x):
    if x['tile_size'] == '1X1':
        return 'switch_' + str(x['name']) + '_sprites'

def GraphicNorth(x):
    if x['tile_size'] != '1X1':
        return 'switch_' + str(x['name']) + '_north_sprites'

def GraphicEast(x):
    if x['tile_size'] == '2X2' or x['tile_size'] == '1x2':
        return 'switch_' + str(x['name']) + '_east_sprites'

def GraphicWest(x):
    if x['tile_size'] == '2X2' or x['tile_size'] == '2x1':
        return 'switch_' + str(x['name']) + '_west_sprites'

def GraphicSouth(x):
    if x['tile_size'] == '2X2':
        return 'switch_' + str(x['name']) + '_south_sprites'

def TileSize(x):
    return 'HOUSE_SIZE_' + x['tile_size']

def TownZones(x):
    townzones = {
        "all" : "ALL_TOWNZONES",
        "4,3,2,1" : "ALL_TOWNZONES & ~bitmask(TOWNZONE_EDGE)",
        "4,3,2" : "bitmask(TOWNZONE_CENTRE, TOWNZONE_INNER_SUBURB, TOWNZONE_OUTER_SUBURB)",
        "4,3" : "bitmask(TOWNZONE_CENTRE, TOWNZONE_INNER_SUBURB)",
        "4 only" : "bitmask(TOWNZONE_CENTRE)",
        "3,2,1" : "bitmask(TOWNZONE_INNER_SUBURB, TOWNZONE_OUTER_SUBURB, TOWNZONE_OUTSKIRT)",
        "3,2" : "bitmask(TOWNZONE_INNER_SUBURB, TOWNZONE_OUTER_SUBURB)",
        "2,1,0" : "bitmask(TOWNZONE_OUTER_SUBURB , TOWNZONE_OUTSKIRT, TOWNZONE_EDGE)",
        "2,1" : "bitmask(TOWNZONE_OUTER_SUBURB , TOWNZONE_OUTSKIRT)",
        "1,0" : "bitmask(TOWNZONE_OUTSKIRT, TOWNZONE_EDGE)",
        "0 only" : "bitmask(TOWNZONE_EDGE)"
        }
    return townzones[x['townzone_number']]

def AvailabilityMask(x):
    return '[' + x['townzones'] + ', bitmask(CLIMATE_TEMPERATE, CLIMATE_ARCTIC, ABOVE_SNOWLINE, CLIMATE_TROPIC)]'

def ConstructionCheck(x):
    if x['con_check_override'] == 'standard':
        return 'switch_' + str(x['height']) + '_con_check'
    elif x['con_check_override'] != 'none':
        return 'switch_' + str(x['con_check_override']) + '_con_check'

def CargoProduction(x):
    return "func_produce(" + str(x['cargo_pass']) + "," + str(x['cargo_mail']) + ")"

def YearsAvailable(x):
    return '[' + str(x['yearstart']) + ',' + str(x['yearend']) + ']'

def NumLevels(b):
    try:
        return len(buildings[b]["levels"])
    except:
        return 1

def GetPoints(b,colour_era):
    weightings_all_levels = list(buildings[b][colour_era].values()) * NumLevels(b)
    end_points = list(accumulate(weightings_all_levels))
    start_points = [x - y for x, y in zip(end_points, weightings_all_levels)]
    bits = []
    for i in range(len(weightings_all_levels)):
        if weightings_all_levels[i] == 1:
            bits.append(str(start_points[i]))
        else:
            bits.append(str(start_points[i]) + ".." + str(end_points[i] -1))
    return bits

def SpriteDirectionsAB(b):
    random_switch = "\n\trandom_switch (FEAT_HOUSES, SELF, switch_" + b + "_random_sprites) {\n\t\t1: switch_" + b + "_a_sprites;\n\t\t1: switch_" + b +"_b_sprites;\n\t}\n"
    south_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_south_check, SpriteDirectionsSouth()) {\n\t\t4: switch_" + b + "_a_sprites;\n\t\t6: switch_" + b + "_a_sprites;\n\t\t9: switch_" + b + "_b_sprites;\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    east_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_east_check, SpriteDirectionsEast()) {\n\t\t4: switch_" + b + "_a_sprites;\n\t\t6: switch_" + b + "_a_sprites;\n\t\t9: switch_" + b + "_b_sprites;\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    west_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_west_check, SpriteDirectionsWest()) {\n\t\t6: switch_" + b + "_b_sprites;\n\t\t9: switch_" + b + "_a_sprites;\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    north_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_north_check, SpriteDirectionsNorth()) {\n\t\t6: switch_" + b + "_b_sprites;\n\t\t9: switch_" + b + "_a_sprites;\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, SpriteDirections() ) {\n\t\t1: switch_" + b + "_a_sprites;\n\t\t2: switch_" + b + "_b_sprites;\n\t\t3: switch_" + b + \
        "_south_check;\n\t\t4: switch_" + b + "_a_sprites;\n\t\t5: switch_" + b + "_a_sprites;\n\t\t6: switch_" + b + "_west_check;\n\t\t8: switch_" + b + "_b_sprites;\n\t\t9: switch_" + b + \
        "_east_check;\n\t\t10: switch_" + b + "_b_sprites;\n\t\t12: switch_" + b + "_north_check;\n\t\tswitch_" + b + "_random_sprites;\n\t}\n"

    return random_switch + south_direction_ab + east_direction_ab + west_direction_ab + north_direction_ab + direction_ab

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
    df_items['graphics_default'] = df_items.apply(GraphicsDefault, axis=1)
    df_items['graphics_north'] = df_items.apply(GraphicsNorth, axis=1)
    df_items['graphics_east'] = df_items.apply(GraphicsEast, axis=1)
    df_items['graphics_west'] = df_items.apply(GraphicsWest, axis=1)
    df_items['graphics_south'] = df_items.apply(GraphicsSouth, axis=1)
    df_items['townzones'] = df_items.apply(TownZones, axis=1)
    df_items = df_items.drop(columns=['townzone_number', 'flags'])

    items = df_items.set_index('name').T.to_dict('dict')
    
    ExportToJSON(items, 'lib/items.json')

def CreateBuildingsJSON():
    # Import the Dataframes
    df_items = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'folder', 'id', 'include', 'tile_size', 'height', 'newjson', 'recolour'])
    df_properties = pd.read_excel('docs/buildings.ods','items', 
        usecols=['name', 'substitute', 'stringname', 'population', 'accepted_cargos', 'probability', 'yearstart', 'yearend', 'minimum_lifetime', 'townzone_number', 'building_class'])
    df_graphics = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'con_check_override', 'cargo_pass', 'cargo_mail', 'height', 'tile_size'])
    df_old_era = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'old_era_end'])
    df_levels = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'levels'])
    df_variants = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'variants'], dtype={'variants':str})
    df_pal = pd.read_excel('docs/buildings.ods','colours')

    # Modify the data
    df_items['tile_size'] = df_items.apply(TileSize, axis=1)
    df_old_era = df_old_era.dropna()
    df_old_era['old_era_end'] = df_old_era['old_era_end'].astype(int)
    df_levels = df_levels.dropna()
    df_variants = df_variants.dropna()
    df_variants['variants'] = df_variants['variants'].str.replace('$','construction_state')
    df_properties['stringname'] = 'string(' + df_properties['stringname'] + ')'
    df_properties['accepted_cargos'] = '[' + df_properties['accepted_cargos'] + ']'
    df_properties['local_authority_impact'] = 80
    df_properties['removal_cost_multiplier'] = 80
    df_properties['years_available'] = df_properties.apply(YearsAvailable, axis=1)
    df_properties['townzones'] = df_properties.apply(TownZones, axis=1)
    df_properties['availability_mask'] = df_properties.apply(AvailabilityMask, axis=1)
    df_graphics['default'] = df_graphics.apply(GraphicDefault, axis=1)
    df_graphics['graphics_north'] = df_graphics.apply(GraphicNorth, axis=1)
    df_graphics['graphics_east'] = df_graphics.apply(GraphicEast, axis=1)
    df_graphics['graphics_west'] = df_graphics.apply(GraphicWest, axis=1)
    df_graphics['graphics_south'] = df_graphics.apply(GraphicSouth, axis=1)
    df_graphics['construction_check'] = df_graphics.apply(ConstructionCheck, axis=1)
    df_graphics['cargo_production'] = df_graphics.apply(CargoProduction, axis=1)

    # convert excel spreadsheet into dataframe
    df_pal = df_pal[~df_pal['name'].isin(palette_numbers)]
    df_pal = df_pal[~df_pal['name'].isin(['remap', 'include'])]
    df_pal['colours'] = df_pal.apply(NameColumnColour, axis=1)
    df_pal['name'] = df_pal.name.str.removesuffix('_all_colours')
    df_pal['name'] = df_pal.name.str.removesuffix('_old_colours')

    # Drop columns
    df_properties = df_properties.drop(columns=['yearstart', 'yearend','townzone_number','townzones'])
    df_graphics = df_graphics.drop(columns=['height','con_check_override', 'cargo_pass', 'cargo_mail', 'tile_size'])

    # Convert to dictionaries
    buildings = df_items.set_index('name').T.to_dict('dict')
    old_era_end = df_old_era.set_index('name').T.to_dict('dict')
    levels = df_levels.set_index('name').T.to_dict('dict')
    variants = df_variants.set_index('name').T.to_dict('dict')
    building_palettes = df_pal.groupby('name').apply(lambda x: x.set_index('colours').to_dict(orient='index')).to_dict()
    properties = df_properties.set_index('name').T.to_dict('dict')
    graphics = df_graphics.set_index('name').T.to_dict('dict')

    # Combine dictionaries
    for b in old_era_end:
        buildings[b]["end_of_old_era"] = old_era_end[b]["old_era_end"]

    for b in levels:
        buildings[b]["levels"] = levels[b]["levels"].split(",")

    for b in variants:
        buildings[b]["variants"] = eval(variants[b]["variants"])

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

    for b in buildings:
        if buildings[b]["recolour"] == True:
            folder = buildings[b]["folder"]
            buildings[b]["all"] = building_palettes[buildings[b]["folder"]]["all"]
        if b in old_era_end:
            buildings[b]["old"] = building_palettes[buildings[b]["folder"]]["old"]

    for b in buildings:
        buildings[b]["properties"] = properties[b]
        buildings[b]["graphics"] = graphics[b]
        
    buildings = CleanNones(buildings)

    ExportToJSON(buildings, 'lib/new_buildings.json')

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

def CreateColourFiles():
    
    building_palettes = LoadJSON('lib/building_palettes.json')
    items = LoadJSON('lib/items.json')

    buildings_no_recolouring = {items[x]["folder"] for x in items if items[x]["recolour"] == False }
    buildings_recolouring = {items[x]["folder"] for x in items if items[x]["recolour"] == True }

    recolour = LoadJSON('lib/recolour.json')
    remap = {x: recolour[x]["remap"] for x in recolour}

    schema = LoadJSON('lib/buildings.json')

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
                    ground_sprite = schema[b]["ground"]
                    data = data.replace(search_text_ground_snow, ground_sprite)
                    data = data.replace(search_text_ground, ground_sprite)            
                except:
                    pass
                # Override for building sprites
                try:
                    building_sprite = schema[b]["building"]
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
    schema = LoadJSON('lib/buildings.json')
    
    for b in schema:
        variants = list(schema[b]["variants"].keys())
        for v in variants:
            template = open("./src/houses/" + b + "/colours/all.pnml", "rt")
            current_variant = open("./src/houses/" + b + "/variants/" + v +".pnml", "wt")
            for line in template:
                try:
                    if schema[b]["shared_variant_gfx"] == True and ("spritelayout" in line or "sprlay_" in line or "FEAT_HOUSES" in line):
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
            xoff = schema[b]["variants"][v]["xoffset"]
            yoff = schema[b]["variants"][v]["yoffset"]
            with open(r'./src/houses/' + b + '/variants/' + v +'.pnml', 'r') as file:
                data = file.read()
                # Offsets
                data = data.replace(search_text_x, xoff)
                data = data.replace(search_text_y, yoff)
                # Hide Sprites
                try: 
                    hide_sprite = schema[b]["variants"][v]["hide_sprite"]
                except:    
                    data = data.replace(search_text_hide_sprite, "0")
                else:
                    data = data.replace(search_text_hide_sprite, hide_sprite)
                # Construction States
                try:
                    construction_state = schema[b]["variants"][v]["construction_state"]
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
    for b in schema:
        sections = []
        variants = list(schema[b]["variants"].keys())
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
    schema = LoadJSON('lib/buildings.json')
    for b in schema:
        levels_pnml = open("src/houses/" + b + "/levels/all.pnml", "wt")
        levels_pnml.write("\n// " + b + " levels\n")
        levels_pnml.close()
        levels = list(schema[b]["levels"])
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
    schema = LoadJSON('lib/buildings.json')

    old_items = [x for x in items if buildings[x]["newjson"] != True  ]

    buildings_no_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == False }
    buildings_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == True }
    old_colour_buildings = {items[x]["folder"] for x in old_items if items[x]["old_colours"] == True }

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
        variants = list(schema[b]["variants"])
        for v in variants:
            heights = list(schema[b]["heights"]) # 's', 'm', 'l' etc
            n = 0
            for h in heights:
                num_heights = len(schema[b]["heights"][h])
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
                levels = list(schema[b]["heights"].values())[n]
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
        variants = list(schema[b]["variants"])
        for v in variants:
            heights = list(schema[b]["heights"])
            n = 0
            for h in heights:
                num_heights = len(schema[b]["heights"][h])
                # Add the switch line and update details
                f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                if v == 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_old, random_bits % " + str(random_bits_total_old_dict[b] * num_heights) + " ) {\n")
                else:
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_old, random_bits % " + str(random_bits_total_old_dict[b] * num_heights) + " ) {\n")
                f.close()
                levels = list(schema[b]["heights"].values())[n]
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
            variants = list(schema[b]["variants"])
            for v in variants:
                heights = list(schema[b]["heights"])
                n = 0
                for h in heights:
                    # Add the switch line and update details
                    f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                    if v == 'x':
                        f.write("\n\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_sprites, current_year - age) {")
                    else:
                        f.write("\n\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_sprites, current_year - age) {")
                    if v == 'x':
                        f.write("\n0.." + str(schema[b]["end_of_old_era"]) + ": switch_" + b + "_" + h + "_old;")  
                    else:
                        f.write("\n0.." + str(schema[b]["end_of_old_era"]) + ": switch_" + b + "_" + v + "_" + h + "_old;")               
                    if v == 'x':
                        f.write("\nswitch_" + b + "_" + h + "_modern;") 
                    else:
                        f.write("\nswitch_" + b + "_" + v + "_" + h + "_modern;") 
                    # Add bracket at the bottom
                    f.write("\n}")
                    f.close()
                    n = n + 1

def CreateDirectionSwitches():
    schema = LoadJSON('lib/buildings.json')
    # Create a spritedirection file for relevant buildings
    for b in schema:
        heights = list(schema[b]["heights"])
        variants = list(schema[b]["variants"].keys())
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
    for b in schema:
        sections = []
        heights = list(schema[b]["heights"])
        variants = list(schema[b]["variants"].keys())
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
    for b in schema:
        heights = list(schema[b]["heights"])
        variants = list(schema[b]["variants"].keys())
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
    schema = LoadJSON('lib/buildings.json')

    name_switch_buildings = {items[x]["folder"] for x in items if items[x]["name_switch"] != 'none' }

    random_bits_total_all_dict = dictionaries.RandomBitsTotalAllDict()

    for b in name_switch_buildings:
        f = open("./src/houses/" + b + "/switches/name_switches.pnml", "w")
        f.write("\n// " + b + " ALL Names\n")
        f.close()
        variants = list(schema[b]["levels"])
        f = open("./src/houses/" + b + "/switches/name_switches.pnml", "a")
        f.write("\nswitch (FEAT_HOUSES, SELF, name_" + b + ", random_bits % " + str(random_bits_total_all_dict[b] * len(variants)) + " ) { // Ref functions.CreateNameSwitches() \n")
        m = 0
        for v in variants:
            # When there are ranges
            if random_bits_total_all_dict[b] > 1:
                f.write("\t" + str(m) + ".." + str(m + random_bits_total_all_dict[b] - 1) + ": \treturn string(" + str(schema[b]["names"][v]) + ");\n")
                m = m + random_bits_total_all_dict[b]
            # When there is single numbers
            else:
                f.write("\t" + str(m) + ": \treturn string(" + str(schema[b]["names"][v]) + ");\n")
                m = m + 1
        f.write("}\n")
        f.close()

def PnmlCombiner():
    folders = ["levels", "colours", "variants"]

    schema = LoadJSON('lib/buildings.json')

    manual_gfx = copy.deepcopy(schema)
    manual_switches = copy.deepcopy(schema)
    for b in schema:
        try:
            schema[b]["manual_gfx"] == True
        except:
            manual_gfx.pop(b)
        try:
            schema[b]["manual_switches"] == True
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

    for b in schema:
        variants = list(schema[b]["variants"].keys())
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

    newjsonbuildings = [x for x in buildings if buildings[x]["newjson"] == True ]

    old_items = [x for x in items if buildings[x]["newjson"] != True  ]

    active_building_names = [x for x in old_items if items[x]["include"] == True]
    active_building_folders = {items[x]["folder"] for x in old_items if items[x]["include"] == True}
    parameter_buildings = [x for x in old_items if items[x]["param_top"] != 'none']

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

    for b in old_items:
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
            data = data.replace('_id_', str(items[b]["id"]))
            data = data.replace('iXj', str(items[b]["tile_size"]))
            data = data.replace('_stringname_', str(items[b]["stringname"]))
            data = data.replace('_population_', str(items[b]["population"]))
            data = data.replace('_probability_', str(items[b]["probability"]))
            data = data.replace('_substitute_', str(items[b]["substitute"]))
            data = data.replace('_building_class_', str(items[b]["building_class"]))
            data = data.replace('_yearstart_', str(items[b]["yearstart"]))
            data = data.replace('_yearend_', str(items[b]["yearend"]))
            data = data.replace('_minimum_lifetime_', str(items[b]["minimum_lifetime"]))
            data = data.replace('height', str(items[b]["height"]))
            data = data.replace('_townzones_', str(items[b]["townzones"]))
            data = data.replace('_building_flags_', str(items[b]["building_flags"]))
            data = data.replace('graphics_default_snow', str(items[b]["graphics_default"]) + "_sprites")
            data = data.replace('graphics_north_snow', str(items[b]["graphics_north"]) + "_sprites")
            data = data.replace('graphics_east_snow', str(items[b]["graphics_east"]) + "_sprites")
            data = data.replace('graphics_west_snow', str(items[b]["graphics_west"]) + "_sprites")
            data = data.replace('graphics_south_snow', str(items[b]["graphics_south"]) + "_sprites")
            data = data.replace('_cargo_pass_', str(items[b]["cargo_pass"]))
            data = data.replace('_cargo_mail_', str(items[b]["cargo_mail"]))
            data = data.replace('_accepted_cargoes_', str(items[b]["accepted_cargos"]))
            data = data.replace('_protection_', str(items[b]["protection"]))
            data = data.replace('_nameswitch_', str(items[b]["name_switch"]))

            if items[b]["con_check_override"] == "standard":
                data = data.replace('_con_check_', str(items[b]["height"]))
            else:
                data = data.replace('_con_check_', str(items[b]["con_check_override"]))
        
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
        top =  items[b]["param_top"]
        bottom =  items[b]["param_bottom"]
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

def CreateBuildingFiles():
    recolour = LoadJSON(recolourJSON)

    newjsonbuildings = [x for x in buildings if buildings[x]["newjson"] == True ]

    # Create Building PNML File
    for b in newjsonbuildings:
        with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'w') as file:
            file.write("\n" + "// " + b + "\n")
            file.close()

    # Create Spritelayouts
    climates = ["norm","snow"]

    for b in newjsonbuildings:
         with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'a') as file:
            file.write("\n// Spritelayouts")
            for v in buildings[b]["variants"]:
                file.write("\n\t// " + v)
                for l in buildings[b]["levels"]:
                    file.write("\n\t\t// " + l)
                    for c in buildings[b]["all"]:
                        file.write("\n\t\t\t// " + c)
                        for k in climates:
                            file.write("\n\t\t\t\t// " + k)
                            file.write("\n\t\t\t\tspritelayout sprlay_" + b + "_" + v + "_" + l + "_" + c + "_" + k + " {\n\t\t\t\t\tground {")
                            file.write("\n\t\t\t\t\t\tsprite: spr_" + buildings[b]["folder"] + "_" + v + "_ground_" + k)
                            try:
                                file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                            except:
                                file.write(" (construction_state);")
                            file.write("\n\t\t\t\t\t}\n\t\t\t\tbuilding {\n\t\t\t\t\t\tsprite: spr_" + b + "_" + v + "_" + l +"_" + k)
                            try:
                                file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                            except:
                                file.write(" (construction_state);")
                            file.write("\n\t\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;")
                            file.write("\n\t\t\t\t\t\tpalette: recolour_remap + " + str(recolour[c]["remap"]) + ";")
                            file.write("\n\t\t\t\t\t}\n\t\t\t}\n")
                        file.write("\n\t\t\t\tswitch(FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + l + "_" + c + "_snow, terrain_type) {\n\t\t\t\t\tTILETYPE_SNOW: sprlay_" + b + "_" + v + "_" + l + "_" + c + "_snow;\n\t\t\t\t\tsprlay_" + b + "_" + v + "_" + l + "_" + c + "_norm;\n\t\t\t\t}\n")
            file.write("\n")
            file.close()

    # Create Colour Switches
    for b in newjsonbuildings:
        if b in [b for b in buildings if buildings[b]["recolour"] == True]:
            with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'a') as file:
                file.write("\n// Colour Switches")
                if "end_of_old_era" in buildings[b]:
                    colour_options = ["all","old"]   
                else:
                    colour_options = ["sprites"]
                for v in buildings[b]["variants"]:
                    for o in colour_options:
                        if o == "all" or o =="sprites":
                            points = GetPoints(b,"all")
                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + o + ", random_bits % " + str(len(buildings[b]["levels"]) * sum(buildings[b]["all"].values())) + " ) { ")
                            i = 0
                            for l in buildings[b]["levels"]:
                                for c in buildings[b]["all"]:
                                    file.write("\n\t\t" + points[i] + ":\tswitch_" + b + "_" + v + "_" + l +"_" + c + "_snow;")
                                    i = i + 1
                        else:
                            points = GetPoints(b,"old")
                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + o + ", random_bits % " + str(len(buildings[b]["levels"]) * sum(buildings[b]["old"].values())) + " ) { ")
                            i = 0
                            for l in buildings[b]["levels"]:
                                for c in buildings[b]["old"]:
                                    file.write("\n\t\t" + points[i] +":\tswitch_" + b + "_" + v + "_" + l +"_" + c + "_snow;")
                                    i = i + 1
                        file.write("\n\t}")
                
                # Switches
                if "end_of_old_era" in buildings[b]:
                    for  v in buildings[b]["variants"]:
                        file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_sprites, current_year - age) {\n\t\t0.." + str(buildings[b]["end_of_old_era"]) + ": switch_" + b + "_" + v + "_old;\n\t\tswitch_" + b + "_" + v + "_all;\n\t}")

                file.write("\n")
                file.close()

    # Create Directions Switches
    for b in newjsonbuildings:
        # For A and B variants
        if list(buildings[b]["variants"].keys()) == ["a", "b"]:
            with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'a') as file:
                file.write("\n// Direction Switches")
                file.write("\n\t"+ SpriteDirectionsAB(b))
                file.close()


    # Create Item Block
    for b in newjsonbuildings:
        with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'a') as file:
            file.write("\n// Item Block\n\titem(FEAT_HOUSES, item_" + b + ", " + str(buildings[b]["id"]) + ", " + str(buildings[b]["tile_size"])  + "){")
            file.write("\n\t\tproperty {")
            file.write("\n\t\t\tsubstitute:\t\t\t\t\t" + str(buildings[b]["properties"]["substitute"]) + ";")
            file.write("\n\t\t\tname:\t\t\t\t\t\t" + str(buildings[b]["properties"]["stringname"]) + ";")
            file.write("\n\t\t\tpopulation:\t\t\t\t\t" + str(buildings[b]["properties"]["population"]) + ";")
            file.write("\n\t\t\taccepted_cargos:\t\t\t" + str(buildings[b]["properties"]["accepted_cargos"]) + ";")
            file.write("\n\t\t\tlocal_authority_impact:\t\t" + str(buildings[b]["properties"]["local_authority_impact"]) + ";")
            file.write("\n\t\t\tremoval_cost_multiplier:\t" + str(buildings[b]["properties"]["removal_cost_multiplier"]) + ";")
            file.write("\n\t\t\tprobability:\t\t\t\t" + str(buildings[b]["properties"]["probability"]) + ";")
            file.write("\n\t\t\tyears_available:\t\t\t" + str(buildings[b]["properties"]["years_available"]) + ";")
            file.write("\n\t\t\tminimum_lifetime:\t\t\t" + str(buildings[b]["properties"]["minimum_lifetime"]) + ";")
            file.write("\n\t\t\tavailability_mask:\t\t\t" + str(buildings[b]["properties"]["availability_mask"]) + ";")
            file.write("\n\t\t\tbuilding_class:\t\t\t\t" + str(buildings[b]["properties"]["building_class"]) + ";")
            file.write("\n\t\t\t}\n\t\tgraphics {")
            try:
                file.write("\n\t\t\tdefault:\t\t\t\t\t" + str(buildings[b]["graphics"]["default"]) + ";")
            except:
                try:
                    file.write("\n\t\t\tgraphics_north:\t\t\t\t\t" + str(buildings[b]["graphics"]["graphics_north"]) + ";")
                except:
                    pass
            try:
                file.write("\n\t\t\tgraphics_east:\t\t\t\t\t" + str(buildings[b]["graphics"]["graphics_east"]) + ";")
            except:
                pass
            try:
                file.write("\n\t\t\tgraphics_west:\t\t\t\t\t" + str(buildings[b]["graphics"]["graphics_west"]) + ";")
            except:
                pass
            try:
                file.write("\n\t\t\tgraphics_south:\t\t\t\t\t" + str(buildings[b]["graphics"]["graphics_south"]) + ";")
            except:
                pass
            try:
                file.write("\n\t\t\tconstruction_check:\t\t\t" + str(buildings[b]["graphics"]["construction_check"]) + ";")
            except:
                pass
            file.write("\n\t\t\tcargo_production:\t\t\t" + str(buildings[b]["graphics"]["cargo_production"]) + ";")

            file.write("\n\t\t}\n}\n")
            file.close()
