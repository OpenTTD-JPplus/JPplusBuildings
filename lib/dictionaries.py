import copy, itertools
import pandas as pd
from buildings import buildings_dict as buildings
from lib import functions, lists

def ColourRemapsDict():
    # convert excel spreadsheet into dataframe
    df1 = pd.read_excel('docs/buildings.ods','colours')
    # convert dataframe into dictionary
    raw_colour_profiles = df1.set_index('name').T.to_dict('dict')

    # REMAPS - get colours with their remap number
    colour_remaps = raw_colour_profiles['remap']
    return colour_remaps

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

def PaletteDict():
    # convert excel spreadsheet into dataframe
    df1 = pd.read_excel('docs/buildings.ods','colours')
    # convert dataframe into dictionary
    raw_colour_profiles = df1.set_index('name').T.to_dict('dict')

    keys = list(recolour_codes.keys())

    palette = {}
    for p in raw_colour_profiles:
        if p in recolour_codes:
            palette[p] = raw_colour_profiles[p]
        else:
            pass
    
    colour_remaps = ColourRemapsDict()

    # Convert colour codes to two digit strings
    for p in palette:
        for c in colour_remaps:
            if len(str(palette[p][c])) == 2:
                palette[p][c] = str(palette[p][c])
            else:
                palette[p][c] = str("0" + str(palette[p][c]))
    return palette

def RecolourDict():
    # convert excel spreadsheet into dataframe
    df1 = pd.read_excel('docs/buildings.ods','colours')
    # convert dataframe into dictionary
    raw_colour_profiles = df1.set_index('name').T.to_dict('dict')

    keys = list(recolour_codes.keys())
    colour_profiles = {}
    for i in raw_colour_profiles:
        if i in keys or i == 'remap':
            pass
        else:
            colour_profiles[i] = raw_colour_profiles[i]           
    
    # Remove colours with nil probability
    for b in colour_profiles:
        colour_profiles[b] = {keys:values for keys, values in colour_profiles[b].items() if values != 0}
    return colour_profiles

def ColourAllDict():
    buildings_recolouring = lists.Recolouring()
    colour_profiles = RecolourDict()

    colour_all_dict = {}
    for b in buildings_recolouring:
        colour_all_dict[b] = colour_profiles[b + "_all_colours"]
    # {'dense_townhouses': {'grey': 2, 'brown1': 2, 'brown2': 2, 'mauve': 1, 'peach': 1, 'black': 2, 'red_brown': 1},
    return colour_all_dict

def ColourOldDict():
    old_colour_buildings = lists.HasOldColours()
    colour_profiles = RecolourDict()

    colour_old_dict = {}
    for b in old_colour_buildings:
        colour_old_dict[b] = colour_profiles[b + "_old_colours"]
    # {'naganuma': {'grey': 2, 'brown1': 2, 'brown2': 2, 'mauve': 1, 'black': 2, 'red_brown': 1},
    return colour_old_dict

def ColourWeightingsAllDict():    
    buildings_recolouring = lists.Recolouring()
    colour_all_dict = ColourAllDict()

    colour_weightings_all_dict = {}
    for b in buildings_recolouring:
        colours = list(colour_all_dict[b].keys())
        for c in colours:
            colour_weightings_all_dict[b] = list(colour_all_dict[b].values())
    # {'aoki_office': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'aoyama_office': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'bank_building': [2, 1],
    return colour_weightings_all_dict

def ColourWeightingsOldDict():
    old_colour_buildings = lists.HasOldColours()
    colour_old_dict = ColourOldDict()

    colour_weightings_old_dict = {}
    for b in old_colour_buildings:
        colours = list(colour_old_dict[b].keys())
        for c in colours:
            colour_weightings_old_dict[b] = list(colour_old_dict[b].values())
    # {'naganuma': [2, 2, 2, 1, 2, 1], 'nishikawa': [1, 1, 1, 1, 1, 1, 1], 'aoki_office': [1, 2, 2, 2, 1, 1, 1],
    return colour_weightings_old_dict

def HeightsDict():
    heights_dict = {}
    for b in buildings:
        heights = list(buildings[b]["heights"])
        for h in heights:
            heights_dict[b] = (buildings[b]["heights"])
    # {'aoki_office': {'m': ['6L'], 'l': ['8L'], 'x': ['10L', '12L']},
    return heights_dict

def NumHeightsDict():
    heights_dict = HeightsDict()
    num_heights_dict = copy.deepcopy(heights_dict)
    for b in heights_dict:
        heights = list(heights_dict[b].keys())
        for h in heights:
            num_heights_dict[b][h] = len(heights_dict[b][h]) 
    # {'fukuda': {'m': 1, 'l': 1}, 'harada': {'m': 1, 'l': 1}, 'hayashi': {'s': 2, 'm': 2}, 'hirano': {'s': 2, 'm': 2}}
    return num_heights_dict

def ColoursAllWeightings():
    buildings_recolouring = lists.Recolouring()
    colour_weightings_all_dict = ColourWeightingsAllDict()
    num_heights_dict = NumHeightsDict()

    colours_all_weightings = {}
    for b in buildings_recolouring:
        heights = num_heights_dict[b]
        colours_all_weightings[b] = num_heights_dict[b]
        for h in heights:
            colours_all_weightings[b][h] = colour_weightings_all_dict[b] * num_heights_dict[b][h]
    # 'fukuda': {'m': [2, 1], 'l': [2, 1]}, 'harada': {'m': [1, 1, 1, 1, 1, 1, 1], 'l': [1, 1, 1, 1, 1, 1, 1]}, 'hasegawa': {'m': [1, 1], 'l': [1, 1]},
    return colours_all_weightings

def ColoursOldWeightings():
    old_colour_buildings = lists.HasOldColours()
    colour_weightings_old_dict = ColourWeightingsOldDict()
    num_heights_dict = NumHeightsDict()

    colours_old_weightings = {}
    for b in old_colour_buildings:
        heights = num_heights_dict[b]
        colours_old_weightings[b] = num_heights_dict[b]
        for h in heights:
            colours_old_weightings[b][h] = colour_weightings_old_dict[b] * num_heights_dict[b][h]
    # 'hirata': {'s': [1, 2, 2, 2, 1, 1, 2, 2, 2, 1], 'm': [1, 2, 2, 2, 1, 1, 2, 2, 2, 1]}, 'kimura': {'s': [1, 2, 2, 2, 1, 1, 2, 2, 2, 1], 'm': [1, 2,
    return colours_old_weightings

def EndPointAll():
    buildings_recolouring = lists.Recolouring()
    colours_all_weightings = ColoursAllWeightings()

    end_point_all = {}
    for b in buildings_recolouring:
        heights = colours_all_weightings[b]
        end_point_all[b] = heights 
        for h in heights:
            end_point_all[b][h] = list(itertools.accumulate(colours_all_weightings[b][h]))
            end_point_all[b][h] = [x - 1 for x in end_point_all[b][h]]
    # 'tetsui': {'s': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'm': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
    return end_point_all

def EndPointOld():
    old_colour_buildings = lists.HasOldColours()
    colours_old_weightings = ColoursOldWeightings()

    end_point_old = {}
    for b in old_colour_buildings:
        heights = colours_old_weightings[b]
        end_point_old[b] = heights 
        for h in heights:
            end_point_old[b][h] = list(itertools.accumulate(colours_old_weightings[b][h]))
            end_point_old[b][h] = [x - 1 for x in end_point_old[b][h]]
    # 'aoki_office': {'m': [0, 2, 4, 6, 7, 8, 9], 'l': [0, 2, 4, 6, 7, 8, 9], 'x': [0, 2, 4, 6, 7, 8, 9, 10, 12, 14, 16, 17, 18, 19]}
    return end_point_old     

def StartPointAll():
    buildings_recolouring = lists.Recolouring()
    colours_all_weightings = ColoursAllWeightings()
    end_point_all = EndPointAll()

    start_point_all = {}
    for b in buildings_recolouring:
        heights = end_point_all[b]
        start_point_all[b] = heights
        # For ALL colours
        for h in heights:
            bits = list(start_point_all[b][h])
            n = 0
            for g in bits:
                start_point_all[b][h][n] = end_point_all[b][h][n] - ( colours_all_weightings[b][h][n] - 1)
                n = n + 1
    # 'fukuda': {'m': [0, 2], 'l': [0, 2]}, 'harada': {'m': [0, 1, 2, 3, 4, 5, 6], 'l': [0, 1, 2, 3, 4, 5, 6]}
    return start_point_all

def StartPointOld():
    old_colour_buildings = lists.HasOldColours()
    colours_old_weightings = ColoursOldWeightings()
    end_point_old = EndPointOld()

    start_point_old = {}
    for b in old_colour_buildings:
        heights = end_point_old[b]
        start_point_old[b] = heights
        # For OLD colours
        for h in heights:
            m = 0
            bits_old = list(start_point_old[b][h])
            for f in bits_old: 
                start_point_old[b][h][m] = end_point_old[b][h][m] - ( colours_old_weightings[b][h][m] - 1)
                m = m + 1
    return start_point_old

def RandomBitsAllRange():
    buildings_recolouring = lists.Recolouring()
    end_point_all = EndPointAll()
    start_point_all = StartPointAll()

    random_bits_all_range = {}
    for b in buildings_recolouring:
        heights = end_point_all[b]
        random_bits_all_range[b] = heights
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
    # {'dense_townhouses': {'h': ['0..1', '2..3', '4..5', '6', '7',
    return random_bits_all_range

def RandomBitsOldRange():
    old_colour_buildings = lists.HasOldColours()
    end_point_old = EndPointOld()
    start_point_old = StartPointOld()
    
    random_bits_old_range = {}
    for b in old_colour_buildings:
        heights = end_point_old[b]
        random_bits_old_range[b] = heights
        # For OLD colours
        for h in heights:
            m = 0
            bits = list(start_point_old[b][h])
            for f in bits: 
                if start_point_old[b][h][m] == end_point_old[b][h][m]:
                    random_bits_old_range[b][h][m] = str(start_point_old[b][h][m])
                else:
                    random_bits_old_range[b][h][m] = str(start_point_old[b][h][m]) + ".." + str(end_point_old[b][h][m])
                m = m + 1
    # {'naganuma': {'h': ['0..1', '2..3', '4..5', '6', '7..8', '9', '10..11', '12..13',        
    return random_bits_old_range

def RandomBitsTotalAllDict():
    buildings_recolouring = lists.Recolouring()
    colour_weightings_all_dict = ColourWeightingsAllDict()

    random_bits_total_all_dict = {}
    for b in buildings_recolouring:
        random_bits_total_all_dict[b] = sum(colour_weightings_all_dict[b])
    # {'dense_townhouses': 11, 'dense_wooden': 2, 'large_wooden_farmhouse': 2,
    return random_bits_total_all_dict

def RandomBitsTotalOldDict():
    old_colour_buildings = lists.HasOldColours()
    colour_weightings_old_dict = ColourWeightingsOldDict()
    
    random_bits_total_old_dict = {}
    for b in old_colour_buildings:
        random_bits_total_old_dict[b] = sum(colour_weightings_old_dict[b])
    # {'naganuma': 10, 'nishikawa': 7, 'aoki_office': 10, 'aoyama_office': 10, 'hirano': 10,
    return random_bits_total_old_dict

def ItemsTab():
    # Import Desired columns
    df1 = pd.read_excel('docs/buildings.ods','items', usecols=[
        'name', 
        'folder', 
        'id',
        'include', 
        'tile_size', 
        'height', 
        'recolour',
        'old_colours',
        'stringname', 
        'population', 
        'probability', 
        'substitute', 
        'building_class',
        'building_flags',
        'yearstart', 
        'yearend', 
        'minimum_lifetime',
        'townzones',
        'cargo_pass',
        'cargo_mail',
        'accepted_cargoes',
        'protection',
        'con_check_override',
        'param_top',
        'param_bottom'
        ])
    all_buildings = df1.set_index('name').T.to_dict('dict')
    # Add graphics columns
    for b in all_buildings:
        # Graphics Default
        if all_buildings[b]['tile_size'] != "1X1":
            all_buildings[b]['graphics_default'] = 'none'
        else:
            if all_buildings[b]['recolour'] == True:
                if all_buildings[b]['height'] == 'skyscraper':
                    all_buildings[b]['graphics_default'] = str(b + '_c')
                elif all_buildings[b]['height'] == 'landmark':
                    all_buildings[b]['graphics_default'] = str(b + '_k')
                elif all_buildings[b]['height'] == 'house':
                    all_buildings[b]['graphics_default'] = str(b + '_h')
                else:
                    all_buildings[b]['graphics_default'] = str(b)
            else:
                all_buildings[b]['graphics_default'] = str(b)
        # Graphics North
        if all_buildings[b]['tile_size'] == "1X1":
            all_buildings[b]['graphics_north'] = 'none'
        else:
            if all_buildings[b]['recolour'] == True:
                if all_buildings[b]['height'] == 'skyscraper':
                    all_buildings[b]['graphics_north'] = str(b + '_c_north')
                elif all_buildings[b]['height'] == 'landmark':
                    all_buildings[b]['graphics_north'] = str(b + '_k_north')
                elif all_buildings[b]['height'] == 'house':
                    all_buildings[b]['graphics_north'] = str(b + '_h_north')
                else:
                    all_buildings[b]['graphics_north'] = str(b + "_north")
            else:
                all_buildings[b]['graphics_north'] = str(b + "_north")
        # Graphics East
        if all_buildings[b]['tile_size'] == "1X1" or all_buildings[b]['tile_size'] == "2X1":
            all_buildings[b]['graphics_east'] = 'none'
        else:
            if all_buildings[b]['recolour'] == True:
                if all_buildings[b]['height'] == 'skyscraper':
                    all_buildings[b]['graphics_east'] = str(b + '_c_east')
                elif all_buildings[b]['height'] == 'landmark':
                    all_buildings[b]['graphics_east'] = str(b + '_k_east')
                elif all_buildings[b]['height'] == 'house':
                    all_buildings[b]['graphics_east'] = str(b + '_h_east')
                else:
                    all_buildings[b]['graphics_east'] = str(b + "_east")
            else:
                all_buildings[b]['graphics_east'] = str(b + "_east")
        # Graphics West
        if all_buildings[b]['tile_size'] == "1X1" or all_buildings[b]['tile_size'] == "1X2":
            all_buildings[b]['graphics_west'] = 'none'
        else:
            if all_buildings[b]['recolour'] == True:
                if all_buildings[b]['height'] == 'skyscraper':
                    all_buildings[b]['graphics_west'] = str(b + '_c_west')
                elif all_buildings[b]['height'] == 'landmark':
                    all_buildings[b]['graphics_west'] = str(b + '_k_west')
                elif all_buildings[b]['height'] == 'house':
                    all_buildings[b]['graphics_west'] = str(b + '_h_west')
                else:
                    all_buildings[b]['graphics_west'] = str(b + "_west")
            else:
                all_buildings[b]['graphics_west'] = str(b + "_west")
        # Graphics South
        if all_buildings[b]['tile_size'] != "2X2":
            all_buildings[b]['graphics_south'] = 'none'
        else:
            if all_buildings[b]['recolour'] == True:
                if all_buildings[b]['height'] == 'skyscraper':
                    all_buildings[b]['graphics_south'] = str(b + '_c_south')
                elif all_buildings[b]['height'] == 'landmark':
                    all_buildings[b]['graphics_south'] = str(b + '_k_south')
                elif all_buildings[b]['height'] == 'house':
                    all_buildings[b]['graphics_south'] = str(b + '_h_south')
                else:
                    all_buildings[b]['graphics_south'] = str(b + "_south")
            else:
                all_buildings[b]['graphics_south'] = str(b + "_south")
    return all_buildings