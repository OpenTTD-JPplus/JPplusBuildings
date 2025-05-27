
import json
from itertools import accumulate

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

def NumLevels(buildings,b):
    try:
        return len(buildings[b]["levels"])
    except:
        return 1

def GetPoints(buildings,b,colour_era):
    weightings_all_levels = list(buildings[b]["colours"][colour_era].values()) * NumLevels(buildings, b)
    end_points = list(accumulate(weightings_all_levels))
    start_points = [x - y for x, y in zip(end_points, weightings_all_levels)]
    bits = []
    for i in range(len(weightings_all_levels)):
        if weightings_all_levels[i] == 1:
            bits.append(str(start_points[i]))
        else:
            bits.append(str(start_points[i]) + ".." + str(end_points[i] -1))
    return bits

def GetPointsComboLevels(buildings,b,levels):
    #weightings_all_levels = list(buildings[b]["colours"][colour_era].values())
    end_points = list(accumulate(levels))
    start_points = [x - y for x, y in zip(end_points, levels)]
    bits = []
    for i in range(len(levels)):
        if levels[i] == 1:
            bits.append(str(start_points[i]))
        else:
            bits.append(str(start_points[i]) + ".." + str(end_points[i] -1))
    return bits

def GetPointsLevels(buildings,b,colour_era):
    width_of_level = sum(buildings[b]["colours"][colour_era].values())
    number_of_levels = NumLevels(buildings,b)
    bits = []
    s = 0
    for i in range(number_of_levels):
        if width_of_level > 1:
            bits.append(str(s) + '..' + str(s + width_of_level - 1) + ':')
            s = s + width_of_level
        else:
            bits.append(str(s) + ':')
            s = s + width_of_level
    return bits

def SpriteDirectionsAB(b):
    random_switch = "\n\trandom_switch (FEAT_HOUSES, SELF, switch_" + b + "_random_sprites) {" + \
        "\n\t\t1: switch_" + b + "_a_sprites;" + \
        "\n\t\t1: switch_" + b +"_b_sprites;\n\t}\n"
    
    south_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_south_check, SpriteDirectionsSouth()) {" + \
        "\n\t\t4: switch_" + b + "_a_sprites;" + \
        "\n\t\t6: switch_" + b + "_a_sprites;" + \
        "\n\t\t9: switch_" + b + "_b_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    
    east_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_east_check, SpriteDirectionsEast()) {" + \
        "\n\t\t4: switch_" + b + "_a_sprites;" + \
        "\n\t\t6: switch_" + b + "_a_sprites;" + \
        "\n\t\t9: switch_" + b + "_b_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    
    west_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_west_check, SpriteDirectionsWest()) {" + \
        "\n\t\t6: switch_" + b + "_b_sprites;" + \
        "\n\t\t9: switch_" + b + "_a_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    
    north_direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_north_check, SpriteDirectionsNorth()) {" + \
        "\n\t\t6: switch_" + b + "_b_sprites;" + \
        "\n\t\t9: switch_" + b + "_a_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    
    direction_ab = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, SpriteDirections() ) {" + \
        "\n\t\t1: switch_" + b + "_a_sprites;" + \
        "\n\t\t2: switch_" + b + "_b_sprites;" + \
        "\n\t\t3: switch_" + b + "_south_check;" + \
        "\n\t\t4: switch_" + b + "_a_sprites;" + \
        "\n\t\t5: switch_" + b + "_a_sprites;" + \
        "\n\t\t6: switch_" + b + "_west_check;" + \
        "\n\t\t8: switch_" + b + "_b_sprites;" + \
        "\n\t\t9: switch_" + b + "_east_check;" + \
        "\n\t\t10: switch_" + b + "_b_sprites;" + \
        "\n\t\t12: switch_" + b + "_north_check;" + \
        "\n\t\tswitch_" + b + "_random_sprites;\n\t}\n"

    return random_switch + south_direction_ab + east_direction_ab + west_direction_ab + north_direction_ab + direction_ab

def SpriteDirectionsABENSW(b):
    random_switch = "\n\trandom_switch (FEAT_HOUSES, SELF, switch_" + b + "_random_sprites) {\n\t\t1: switch_" + b + "_a_sprites;\n\t\t1: switch_" + b +"_b_sprites;\n\t}\n"
    direction_abensw = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, SpriteDirections() ) {" + \
        "\n\t\t1:  switch_" + b + "_a_sprites;" + \
        "\n\t\t2:  switch_" + b + "_b_sprites;" + \
        "\n\t\t3:  switch_" + b + "_s_sprites;" + \
        "\n\t\t4:  switch_" + b + "_a_sprites;" + \
        "\n\t\t5:  switch_" + b + "_a_sprites;" + \
        "\n\t\t6:  switch_" + b + "_w_sprites;" + \
        "\n\t\t7:  switch_" + b + "_a_sprites;" + \
        "\n\t\t8:  switch_" + b + "_b_sprites;" + \
        "\n\t\t9:  switch_" + b + "_e_sprites;" + \
        "\n\t\t10: switch_" + b + "_b_sprites;" + \
        "\n\t\t11: switch_" + b + "_b_sprites;" + \
        "\n\t\t12: switch_" + b + "_n_sprites;" + \
        "\n\t\t13: switch_" + b + "_a_sprites;" + \
        "\n\t\t14: switch_" + b + "_b_sprites;" + \
        "\n\t\tswitch_" + b + "_random_sprites;\n\t}\n"

    return random_switch + direction_abensw

def SpriteDirectionsABS(b):
    random_switch = "\n\trandom_switch (FEAT_HOUSES, SELF, switch_" + b + "_random_sprites) {\n\t\t1: switch_" + b + "_a_sprites;\n\t\t1: switch_" + b +"_b_sprites;\n\t}\n"
    
    east_direction_abs = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_east_check, SpriteDirectionsEast()) {" + \
        "\n\t\t4: switch_" + b + "_a_sprites;" + \
        "\n\t\t6: switch_" + b + "_a_sprites;" + \
        "\n\t\t9: switch_" + b + "_b_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    
    west_direction_abs = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_west_check, SpriteDirectionsWest()) {" + \
        "\n\t\t6: switch_" + b + "_b_sprites;" + \
        "\n\t\t9: switch_" + b + "_a_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"
    
    north_direction_abs = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_north_check, SpriteDirectionsNorth()) {" + \
        "\n\t\t6: switch_" + b + "_b_sprites;" + \
        "\n\t\t9: switch_" + b + "_a_sprites;" + \
        "\n\t\tswitch_" + b +"_random_sprites;\n\t}\n"

    direction_abs = "\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, SpriteDirections() ) {" + \
        "\n\t\t1:  switch_" + b + "_a_sprites;" + \
        "\n\t\t2:  switch_" + b + "_b_sprites;" + \
        "\n\t\t3:  switch_" + b + "_s_sprites;" + \
        "\n\t\t4:  switch_" + b + "_a_sprites;" + \
        "\n\t\t5:  switch_" + b + "_a_sprites;" + \
        "\n\t\t6:  switch_" + b + "_west_check;" + \
        "\n\t\t7:  switch_" + b + "_a_sprites;" + \
        "\n\t\t8:  switch_" + b + "_b_sprites;" + \
        "\n\t\t9:  switch_" + b + "_east_check;" + \
        "\n\t\t10: switch_" + b + "_b_sprites;" + \
        "\n\t\t11: switch_" + b + "_b_sprites;" + \
        "\n\t\t12: switch_" + b + "_north_check;" + \
        "\n\t\t13: switch_" + b + "_a_sprites;" + \
        "\n\t\t14: switch_" + b + "_b_sprites;" + \
        "\n\t\tswitch_" + b + "_random_sprites;\n\t}\n"

    return random_switch + east_direction_abs + west_direction_abs + north_direction_abs + direction_abs