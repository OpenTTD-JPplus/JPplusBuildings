import copy, itertools, json
import pandas as pd
from lib import functions

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

buildingsJSON = 'lib/new_buildings.json'
buildings = LoadJSON(buildingsJSON)

items = LoadJSON('lib/items.json')
old_items = [x for x in items if buildings[x]["newjson"] != True  ]

def ColoursAllWeightings():
    buildings_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == True }

    schema = LoadJSON('lib/buildings.json')
    num_heights_dict = {x: schema[x]["heights"] for x in schema}
    for b in num_heights_dict:
        heights = list(num_heights_dict[b].keys())
        for h in heights:
            num_heights_dict[b][h] = len(num_heights_dict[b][h])

    building_palettes = LoadJSON('lib/building_palettes.json')
    colour_weightings_all_dict = {b: list(building_palettes[b]["all"].values()) for b in building_palettes}

    colours_all_weightings = {}
    for b in buildings_recolouring:
        heights = num_heights_dict[b]
        colours_all_weightings[b] = num_heights_dict[b]
        for h in heights:
            colours_all_weightings[b][h] = colour_weightings_all_dict[b] * num_heights_dict[b][h]
    # 'fukuda': {'m': [2, 1], 'l': [2, 1]}, 'harada': {'m': [1, 1, 1, 1, 1, 1, 1], 'l': [1, 1, 1, 1, 1, 1, 1]}, 'hasegawa': {'m': [1, 1], 'l': [1, 1]},
    return colours_all_weightings

def ColoursOldWeightings():
    old_colour_buildings = {items[x]["folder"] for x in old_items if items[x]["old_colours"] == True }

    schema = LoadJSON('lib/buildings.json')
    num_heights_dict = {x: schema[x]["heights"] for x in schema}
    for b in num_heights_dict:
        heights = list(num_heights_dict[b].keys())
        for h in heights:
            num_heights_dict[b][h] = len(num_heights_dict[b][h])

    building_palettes = LoadJSON('lib/building_palettes.json')
    colour_weightings_old_dict = {b: list(building_palettes[b]["old"].values()) for b in building_palettes if "old" in building_palettes[b].keys() }

    colours_old_weightings = {}
    for b in old_colour_buildings:
        heights = num_heights_dict[b]
        colours_old_weightings[b] = num_heights_dict[b]
        for h in heights:
            colours_old_weightings[b][h] = colour_weightings_old_dict[b] * num_heights_dict[b][h]
    # 'hirata': {'s': [1, 2, 2, 2, 1, 1, 2, 2, 2, 1], 'm': [1, 2, 2, 2, 1, 1, 2, 2, 2, 1]}, 'kimura': {'s': [1, 2, 2, 2, 1, 1, 2, 2, 2, 1], 'm': [1, 2,
    return colours_old_weightings

def EndPointAll():
    buildings_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == True }

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
    old_colour_buildings = {items[x]["folder"] for x in old_items if items[x]["old_colours"] == True }

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
    buildings_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == True }

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
    old_colour_buildings = {items[x]["folder"] for x in old_items if items[x]["old_colours"] == True }

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
    buildings_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == True }

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
    old_colour_buildings = {items[x]["folder"] for x in old_items if items[x]["old_colours"] == True }

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
    buildings_recolouring = {items[x]["folder"] for x in old_items if items[x]["recolour"] == True }

    building_palettes = LoadJSON('lib/building_palettes.json')
    colour_weightings_all_dict = {b: list(building_palettes[b]["all"].values()) for b in building_palettes}

    random_bits_total_all_dict = {}
    for b in buildings_recolouring:
        random_bits_total_all_dict[b] = sum(colour_weightings_all_dict[b])
    # {'dense_townhouses': 11, 'dense_wooden': 2, 'large_wooden_farmhouse': 2,
    return random_bits_total_all_dict

def RandomBitsTotalOldDict():
    old_colour_buildings = {items[x]["folder"] for x in old_items if items[x]["old_colours"] == True }
    
    building_palettes = LoadJSON('lib/building_palettes.json')
    colour_weightings_old_dict = {b: list(building_palettes[b]["old"].values()) for b in building_palettes if "old" in building_palettes[b].keys() }
    
    random_bits_total_old_dict = {}
    for b in old_colour_buildings:
        random_bits_total_old_dict[b] = sum(colour_weightings_old_dict[b])
    # {'naganuma': 10, 'nishikawa': 7, 'aoki_office': 10, 'aoyama_office': 10, 'hirano': 10,
    return random_bits_total_old_dict
