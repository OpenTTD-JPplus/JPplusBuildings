
import json
import pandas as pd

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

def ExportToJSON(dictionary, target_file):
    with open(target_file, 'w') as fp:
        json.dump(dictionary, fp, indent=4)

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

def GraphicDefault(x):
    if x['tile_size'] == '1X1':
        return 'switch_' + str(x['name']) + '_sprites'

def GraphicNorth(x):
    if x['tile_size'] != '1X1':
        return 'switch_' + str(x['name']) + '_n_sprites'

def GraphicEast(x):
    if x['tile_size'] == '2X2' or x['tile_size'] == '1x2':
        return 'switch_' + str(x['name']) + '_e_sprites'

def GraphicWest(x):
    if x['tile_size'] == '2X2' or x['tile_size'] == '2x1':
        return 'switch_' + str(x['name']) + '_w_sprites'

def GraphicSouth(x):
    if x['tile_size'] == '2X2':
        return 'switch_' + str(x['name']) + '_s_sprites'

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

def Protection(x):
    if x['protection'] != 'none':
        return 'switch_' + x['protection'] + '_protection'

### Colour Stuff

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

def NameColumnColour(x):
    if 'old_colours' in x['name']:
        return 'old'
    else:
        return 'all'

def CreateBuildingsJSON():
    # Import the Dataframes
    df_items = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'folder', 'id', 'include', 'tile_size', 'height', 'newjson', 'recolour'])
    df_properties = pd.read_excel('docs/buildings.ods','items', 
        usecols=['name', 'substitute', 'population', 'accepted_cargos', 'probability', 'yearstart', 'yearend', 'minimum_lifetime', 'townzone_number', 'building_class'])
    df_graphics = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'con_check_override', 'cargo_pass', 'cargo_mail', 'height', 'tile_size'])
    df_name_via_prop = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'stringname'])
    df_name_switch = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'name_switch'])
    df_old_era = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'old_era_end'])
    df_manual = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'manual'])
    df_ground = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'ground_override'])
    df_shared_gfx = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'shared_gfx'])
    df_protection = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'protection'])
    df_levels = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'levels'])
    df_variants = pd.read_excel('docs/buildings.ods','items', usecols=['name', 'variants'], dtype={'variants':str})
    df_pal = pd.read_excel('docs/buildings.ods','colours')

    # Modify the data
    df_items['tile_size'] = df_items.apply(TileSize, axis=1)
    df_name_via_prop = df_name_via_prop.dropna()
    df_name_via_prop['stringname'] = 'string(' + df_name_via_prop['stringname'] + ')'
    df_name_switch = df_name_switch.dropna()
    df_old_era = df_old_era.dropna()
    df_old_era['old_era_end'] = df_old_era['old_era_end'].astype(int)
    df_manual = df_manual.dropna()
    df_manual['manual'] = True
    df_ground = df_ground.dropna()
    df_shared_gfx = df_shared_gfx.dropna()
    df_shared_gfx['shared_gfx'] = True
    df_protection = df_protection.dropna()
    df_protection['protection'] = df_protection.apply(Protection, axis=1)
    df_levels = df_levels.dropna()
    df_variants = df_variants.dropna()
    df_variants['variants'] = df_variants['variants'].str.replace('X','xoffset')
    df_variants['variants'] = df_variants['variants'].str.replace('Y','yoffset')
    df_variants['variants'] = df_variants['variants'].str.replace('$','construction_state')
    df_variants['variants'] = df_variants['variants'].str.replace('#','hide_sprite')
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
    name_via_prop = df_name_via_prop.set_index('name').T.to_dict('dict')
    name_switch = df_name_switch.set_index('name').T.to_dict('dict')
    old_era_end = df_old_era.set_index('name').T.to_dict('dict')
    manual = df_manual.set_index('name').T.to_dict('dict')
    ground = df_ground.set_index('name').T.to_dict('dict')
    shared_gfx = df_shared_gfx.set_index('name').T.to_dict('dict')
    protection = df_protection.set_index('name').T.to_dict('dict')
    levels = df_levels.set_index('name').T.to_dict('dict')
    variants = df_variants.set_index('name').T.to_dict('dict')
    building_palettes = df_pal.groupby('name').apply(lambda x: x.set_index('colours').to_dict(orient='index')).to_dict()
    properties = df_properties.set_index('name').T.to_dict('dict')
    graphics = df_graphics.set_index('name').T.to_dict('dict')

    # Combine dictionaries
    for b in old_era_end:
        buildings[b]["end_of_old_era"] = old_era_end[b]["old_era_end"]

    for b in manual:
        buildings[b]["manual"] = manual[b]["manual"]

    for b in ground:
        buildings[b]["ground_override"] = ground[b]["ground_override"]

    for b in shared_gfx:
        buildings[b]["shared_gfx"] = shared_gfx[b]["shared_gfx"]

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

    for b in protection:
        buildings[b]["graphics"]["protection"] = protection[b]["protection"]

    for b in name_via_prop:
        buildings[b]["properties"]["name"] = name_via_prop[b]["stringname"]
    
    for b in name_switch:
        buildings[b]["graphics"]["name"] = eval(name_switch[b]["name_switch"])
        for level in buildings[b]["graphics"]["name"]["names"]:
            buildings[b]["graphics"]["name"]["names"][level] = 'return string(' + str(buildings[b]["graphics"]["name"]["names"][level]) + ')'
    
    buildings = CleanNones(buildings)

    ExportToJSON(buildings, 'lib/new_buildings.json')
