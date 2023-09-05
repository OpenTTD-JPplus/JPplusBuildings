import copy, itertools
import pandas as pd
from lib.buildings_and_colours import buildings_dict as buildings
from lib import functions

def ColourDict():
    buildings_recolouring = functions.Recolouring()

    colour_dict = {}
    for b in buildings_recolouring:
        colours = list(buildings[b]["colours"].keys())
        for c in colours:
            colour_dict[b] = buildings[b]["colours"]
    # {'aoki_office': {'white': 1, 'grey': 2, 'brown1': 2, 'brown2': 2, 'mauve': 1, 'dark_green': 1,
    return colour_dict

def ColourWeightingsAllDict():    
    buildings_recolouring = functions.Recolouring()

    colour_weightings_all_dict = {}
    for b in buildings_recolouring:
        colours = list(buildings[b]["colours"].keys())
        for c in colours:
            colour_weightings_all_dict[b] = list(buildings[b]["colours"].values())
    # {'aoki_office': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'aoyama_office': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'bank_building': [2, 1],
    return colour_weightings_all_dict

def ColourWeightingsOldDict():
    buildings_recolouring = functions.Recolouring()
    buildings_no_recolouring = functions.NoRecolouring()

    colour_weightings_old_dict = {}
    for b in buildings_recolouring:
        colours = list(buildings[b]["colours"].keys())
        for c in colours:
            if buildings[b]["old_colours"] == False:
                colour_weightings_old_dict[b] = False
            else:
                colour_weightings_old_dict[b] = list(buildings[b]["old_colours"].values())
    for b in buildings_no_recolouring:
        colour_weightings_old_dict[b] = False
    colour_weightings_old_dict = dict(sorted(colour_weightings_old_dict.items())) 
    # {'aoki_office': [1, 2, 2, 2, 1, 1, 1], 'aoyama_office': [1, 2, 2, 2, 1, 1, 1], 'bank_building': False,
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
    buildings_recolouring = functions.Recolouring()
    buildings_no_recolouring = functions.NoRecolouring()
    num_heights_dict = NumHeightsDict()
    colour_weightings_all_dict = ColourWeightingsAllDict()
    colour_weightings_all_levels_dict = copy.deepcopy(colour_weightings_all_dict)
    colours_all_weightings = copy.deepcopy(num_heights_dict)
    for b in buildings_recolouring:
        heights = list(colours_all_weightings[b].keys())
        for h in heights:
            colours_all_weightings[b][h] = colour_weightings_all_levels_dict[b] * num_heights_dict[b][h] 
    # colours_all_weightings = {'aoki_office': {'m': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'l': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'x': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1]}, 'aoyama_office': {'m': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1], 'l': [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1]}
    for b in buildings_no_recolouring:
        colours_all_weightings.pop(b)
    
    return colours_all_weightings

def ColoursOldWeightings():
    buildings_recolouring = functions.Recolouring()
    buildings_no_recolouring = functions.NoRecolouring()
    num_heights_dict = NumHeightsDict()
    colours_old_weightings = copy.deepcopy(num_heights_dict)
    colour_weightings_old_dict = ColourWeightingsOldDict()
    colour_weightings_old_levels_dict = copy.deepcopy(colour_weightings_old_dict)
    for b in buildings_recolouring:
        heights = list(colours_old_weightings[b].keys())
        for h in heights:
            if buildings[b]["old_colours"] == False:
                colours_old_weightings[b][h] = False
            else:
                colours_old_weightings[b][h] = colour_weightings_old_levels_dict[b] * num_heights_dict[b][h] 
    # 'hayashi': {'s': False, 'm': False}, 'hirano': {'s': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'm': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]},
    
    for b in buildings_no_recolouring:
        colours_old_weightings.pop(b)

    return colours_old_weightings

def EndPointAll():
    buildings_recolouring = functions.Recolouring()
    colours_all_weightings = ColoursAllWeightings()
    end_point_all = copy.deepcopy(colours_all_weightings)
    for b in buildings_recolouring:
        heights = list(colours_all_weightings[b].keys())
        for h in heights:
            end_point_all[b][h] = list(itertools.accumulate(colours_all_weightings[b][h]))
            end_point_all[b][h] = [x - 1 for x in end_point_all[b][h]]
            
    return end_point_all

def EndPointOld():
    buildings_recolouring = functions.Recolouring()
    colours_old_weightings = ColoursOldWeightings()
    end_point_old = copy.deepcopy(colours_old_weightings)
    for b in buildings_recolouring:
        heights = list(colours_old_weightings[b].keys())
        for h in heights:
            if buildings[b]["old_colours"] == False:
                end_point_old[b][h] = False
            else:
                end_point_old[b][h] = list(itertools.accumulate(colours_old_weightings[b][h]))
                end_point_old[b][h] = [x - 1 for x in end_point_old[b][h]]
    
    return end_point_old

def StartPointAll():
    buildings_recolouring = functions.Recolouring()
    colours_all_weightings = ColoursAllWeightings()
    end_point_all = EndPointAll()
    start_point_all = copy.deepcopy(end_point_all)
    for b in buildings_recolouring:
        heights = list(start_point_all[b].keys())
        # For ALL colours
        for h in heights:
            bits = list(start_point_all[b][h])
            n = 0
            for g in bits:
                start_point_all[b][h][n] = end_point_all[b][h][n] - ( colours_all_weightings[b][h][n] - 1)
                n = n + 1
    return start_point_all

def StartPointOld():
    buildings_recolouring = functions.Recolouring()
    colours_old_weightings = ColoursOldWeightings()
    end_point_old = EndPointOld()
    start_point_old = copy.deepcopy(end_point_old)
    for b in buildings_recolouring:
        heights_old = list(start_point_old[b].keys())
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
    return start_point_old

def RandomBitsAllRange():
    buildings_recolouring = functions.Recolouring()
    end_point_all = EndPointAll()
    start_point_all = StartPointAll()
    random_bits_all_range = copy.deepcopy(end_point_all)
    for b in buildings_recolouring:
        heights = list(random_bits_all_range[b].keys())
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
    return random_bits_all_range

def RandomBitsOldRange():
    buildings_recolouring = functions.Recolouring()
    end_point_old = EndPointOld()
    start_point_old = StartPointOld()
    random_bits_old_range = copy.deepcopy(end_point_old)
    for b in buildings_recolouring:
        heights_old = list(random_bits_old_range[b].keys())
        # For OLD colours
        for i in heights_old:
            m = 0
            if buildings[b]["old_colours"] == False:
                random_bits_old_range[b][i] = False
                m = m + 1
            else:
                bits_old = list(start_point_old[b][i])
                for f in bits_old: 
                    if start_point_old[b][i][m] == end_point_old[b][i][m]:
                        random_bits_old_range[b][i][m] = str(start_point_old[b][i][m])
                    else:
                        random_bits_old_range[b][i][m] = str(start_point_old[b][i][m]) + ".." + str(end_point_old[b][i][m])
                    m = m + 1
    return random_bits_old_range

def RandomBitsTotalAllDict():
    buildings_recolouring = functions.Recolouring()
    random_bits_total_all_dict = {}
    for b in buildings_recolouring:
        random_bits_total_all_dict[b] = sum(buildings[b]["colours"].values())
    return random_bits_total_all_dict

def RandomBitsTotalOldDict():
    buildings_recolouring = functions.Recolouring()
    random_bits_total_old_dict = {}
    for b in buildings_recolouring:
        if buildings[b]["old_colours"] == False:
            random_bits_total_old_dict[b] = False
        else:
            random_bits_total_old_dict[b] = sum(buildings[b]["old_colours"].values())
    return random_bits_total_old_dict

def ItemsTab():
    # Import Desired columns
    df1 = pd.read_excel('docs/buildings.xlsx','items', usecols=[
        'name', 
        'folder', 
        'id', 
        'tile_size', 
        'height', 
        'recolour', 
        'stringname', 
        'population', 
        'probability', 
        'substitute', 
        'building_class', 
        'yearstart', 
        'yearend', 
        'minimum_lifetime',
        'townzones',
        'cargo_pass',
        'cargo_mail',
        'accepted_cargoes',
        'protection'
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