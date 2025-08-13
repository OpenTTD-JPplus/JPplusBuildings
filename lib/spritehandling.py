
import json
from lib.functions import LoadJSON as LoadJSON
from lib.functions import BitsRequired as BitsRequired
from lib.functions import GetPointsBravo as GetPointsBravo
from lib.functions import SpriteDirectionsAB as SpriteDirectionsAB

buildingsJSON = 'lib/buildings.json'
recolourJSON = 'lib/recolour.json'

recolour = LoadJSON(recolourJSON)
buildings = LoadJSON(buildingsJSON)

def SpriteHandling(b,building_file,variants,levels,childsprites):
    with open(building_file, 'a') as file:
        
        # Spritelayouts
        file.write("\n" + "// Spritelayouts\n")
        climates = ['norm', 'snow']
        num_childsprites = len(buildings[b]["childsprites"])

        for v in variants:
            for l in levels:
                file.write("\n\t// " + l )
                for k in climates:
                    file.write("\n\t\t// " + k )
                    file.write("\n\t\t\tspritelayout sprlay_" + b + "_" + v + "_" + l + "_" + k + " {")
                    file.write("\n\t\t\t\tground {\n\t\t\t\t\tsprite:")
                    # Ground graphics incl overrides
                    if 'ground_override' in buildings[b].keys():
                        if '[level]' in buildings[b]["ground_override"]:
                            level_override = buildings[b]["ground_override"]
                            level_override = level_override.replace("[level]",l)
                            file.write(level_override + "_" + k)
                        else:
                            file.write(buildings[b]["ground_override"] + "_" + k)
                    else:
                        file.write("spr_" + buildings[b]["folder"] + "_" + v + "_ground_" + k)
                    # Ground Construction State
                    try:
                        file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                    except:
                        file.write(" (construction_state);")
                    # Building Sprites
                    try:
                        if b in [x for x in buildings if buildings[b]["shared_gfx"] == True]:
                            file.write("\n\t\t\t\t\t}\n\t\t\t\tbuilding {\n\t\t\t\t\tsprite: spr_" + b + "_" + l +"_" + k)
                    except:    
                        file.write("\n\t\t\t\t\t}\n\t\t\t\tbuilding {\n\t\t\t\t\tsprite: spr_" + b + "_" + v + "_" + l +"_" + k)
                    # Buildings Constructiion State
                    try:
                        file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                    except:
                        file.write(" (construction_state);")
                    # Colour Remapping
                    file.write("\n\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;")
                    file.write("\n\t\t\t\t\tpalette: recolour_remap + LOAD_TEMP(0);")
                    # Hide Sprite Check
                    try: 
                        file.write("\n\t\t\t\t\t\thide_sprite: " + str(buildings[b]["variants"][v]["hide_sprite"]) + ";")
                    except:
                        pass
                    # X Offset Check
                    try: 
                        file.write("\n\t\t\t\t\t\txoffset: " + str(buildings[b]["variants"][v]["xoffset"]) + ";")
                    except:
                        pass
                    # Y Offset Check
                    try: 
                        file.write("\n\t\t\t\t\t\tyoffset: " + str(buildings[b]["variants"][v]["yoffset"]) + ";")
                    except:
                        pass
                    file.write("\n\t\t\t\t\t}")
                    # Childsprites
                    if 'childsprites' in list(buildings[b].keys()):
                        for c in childsprites:
                            file.write("\n\t\t\t\tchildsprite { // " + c + "\n\t\t\t\t\tsprite: ")
                            file.write("spr_" + b + "_" + v + "_" + l + "_" + c + "_" + k)
                            # Childsprite Construction State
                            if 'single' in list(buildings[b]["childsprites"][c]["conditions"]):  # If just the one, match what the building does
                                try:
                                    file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + "); // Same as building")
                                except:
                                    file.write(" (construction_state); // Same as building")
                            elif 'seasonal' in list(buildings[b]["childsprites"][c]["conditions"]):
                                if k == 'norm':
                                    file.write(" (LOAD_TEMP(3)); // Seasonal")
                                else:
                                    file.write(" (3); // Seasonal, but winter tree in the snow")
                            else:
                                print("Loose End @ Childsprite Construction States")
                            # Childsprite Recolouring
                            if 'remap' in list(buildings[b]["childsprites"][c]["conditions"]):
                                file.write("\n\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;\n\t\t\t\t\tpalette: recolour_remap + LOAD_TEMP(2);")
                            file.write("\n\t\t\t\t}")
                    file.write("\n\t\t\t}\n")

        # Getbits resolving
        sum_prob_new_colours = sum(buildings[b]["colours"]["new"].values())
        count_new_colours = len(buildings[b]["colours"]["new"])
        if 'old_era_end' in buildings[b]['colours']:
            sum_prob_old_colours = sum(buildings[b]["colours"]["old"].values())
            count_old_colours = len(buildings[b]["colours"]["old"])
        else: 
            sum_prob_old_colours = 0
        if 'fence' in list(buildings[b]['childsprites'].keys()):
            num_fence_colours = len(buildings[b]["colours"]["fence"])
        else:
            num_fence_colours = 0

        file.write("\n/*\n==================\nGetbits Allocation\n==================")

        # Building Colours - old and new
        if 'childsprites' in list(buildings[b].keys()):
            file.write("\nChildsprites: " + str(childsprites)+"\n")
        else:
            file.write("\nChildsprites: 🚫\n")
        if 'old_era_end' in buildings[b]['colours']:
            old_colour_list = list(buildings[b]['colours']['old'].keys())
            file.write("\n" + str(count_old_colours) + " unique Old Colours, Probabilities summing to " + str(sum_prob_old_colours))
            if sum_prob_old_colours in [2,4,8,16] and sum_prob_new_colours == sum_prob_old_colours:
                file.write(" ✅")
            else:
                file.write(" ❌")
                print("❌" + b + " has the wrong sum of probablities: It has " + str(sum_prob_old_colours))
            file.write("\n" + str(old_colour_list) + "\n")
        new_colour_list = list(buildings[b]['colours']['new'].keys())
        file.write("\n" + str(count_new_colours) + " unique New Colours, Probabilities summing to " + str(sum_prob_new_colours))
        if sum_prob_new_colours in [2,4,8,16]:
            file.write(" ✅")
        else:
            file.write(" ❌")
            print("❌" + b + " has the wrong sum of probablities: It has " + str(sum_prob_new_colours))
        file.write("\n" + str(new_colour_list))

        # Fence Colours
        if 'fence' in list(buildings[b]['childsprites'].keys()):
            if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                fence_colour_list =  list(buildings[b]['colours']['fence'].keys())         
                if num_fence_colours == 4:
                    file.write("\n\n4 Fence colours (due to hardcoding) ✅")
                else:
                    file.write("\n\n" + str(num_fence_colours) + " fence colour choices ❌\n")
                    print("❌ " + b + " has the wrong number of fence colour choices. It has " + str(num_fence_colours) )
                file.write("\n" + str(fence_colour_list))

        file.write("\n\nFeature\t\tNum\t\tStart\tBits\tStorage\n------------------------------------------------------------------")
        start_point = 0
        # Levels
        if len(levels) > 1:
            file.write("\nLevels\t\t" + str(len(levels)) + "\t\t" + str(start_point) + "\t\t" + str(BitsRequired(len(levels))) + "\t\t🚫")
            level_start_point = start_point
            start_point = start_point + BitsRequired(len(levels))
        # Building Colours
        if sum_prob_new_colours > 0:
            file.write("\nBuilding\t" + str(sum_prob_new_colours) + "\t\t" + str(start_point) + "\t\t" + str(BitsRequired(sum_prob_new_colours)) + "\t\tLOAD_TEMP(0)" )
            building_colour_start_point = start_point
            start_point = start_point + BitsRequired(sum_prob_new_colours)
        # Fence Colours
        if 'fence' in list(buildings[b]['childsprites'].keys()):
            if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                file.write("\nFence 🎨\t" + str(4) + "\t\t" + str(start_point) + "\t\t" + str(2) + "\t\tLOAD_TEMP(2)")
                fence_colour_start_point = start_point
                start_point = start_point + 2
            
        file.write("\n*/\n")

        file.write("\n// Random Switches")
        file.write("\n\t// Building Colours")
        # Old Colours
        if 'old_era_end' in buildings[b]['colours']:
            file.write("\n\t\tswitch (FEAT_HOUSES, SELF, " + b + "_build_clr_old, getbits(random_bits, " + str(building_colour_start_point) + ", " + str(BitsRequired(sum_prob_new_colours)) + ")) {")
            points = GetPointsBravo(buildings,b,"old")
            i = 0
            for c in old_colour_list:
                if i == len(old_colour_list) - 1:
                    file.write("\n\t\t\t\treturn " + str(recolour[c]['remap']) + ";")
                else:
                    file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
                i = i + 1
            file.write("\n\t\t}")
        # New Colours
        file.write("\n\t\tswitch (FEAT_HOUSES, SELF, " + b + "_build_clr_new, getbits(random_bits, " + str(building_colour_start_point) + ", " + str(BitsRequired(sum_prob_new_colours)) + ")) {")
        points = GetPointsBravo(buildings,b,"new")
        i = 0
        for c in new_colour_list:
            if i == len(new_colour_list) - 1:
                file.write("\n\t\t\t\treturn " + str(recolour[c]['remap']) + ";")
            else:
                file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
            i = i + 1
        file.write("\n\t\t}")
        # Fence Colours
        if 'fence' in list(buildings[b]['childsprites'].keys()):
            if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                file.write("\n\t// Fence Colours")
                file.write("\n\t\tswitch (FEAT_HOUSES, SELF, " + b + "_fence_clr, getbits(random_bits, " + str(fence_colour_start_point) + ", " + str(2) + ")) {")
                points = GetPointsBravo(buildings,b,"fence")
                i = 0
                for c in fence_colour_list:
                    if i == len(fence_colour_list) - 1:
                        file.write("\n\t\t\t\treturn " + str(recolour[c]['remap']) + ";")
                    else:
                        file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
                    i = i + 1
                file.write("\n\t\t}")

        # Switches
        file.write("\n// Spritelayout Switches")
        
        for v in variants:
            file.write("\n\t// " + v)
            for l in levels:
                file.write("\n\t\t// " + l)
                #Header
                if len(levels) > 1:  # If only 1 level, include level in name
                    file.write("\n\t\t\tswitch (FEAT_HOUSES,SELF, switch_" + b + "_" + v + "_" + l + "_sprites, [")
                else:               # Else include level in name
                    file.write("\n\t\t\tswitch (FEAT_HOUSES,SELF, switch_" + b + "_" + v + "_sprites, [")
                # Building Colours
                if 'old_era_end' in buildings[b]['colours']:
                    file.write("\n\t\t\t\tSTORE_TEMP((current_year - age) < " + str(buildings[b]['colours']['old_era_end']) + " ? " + b + "_build_clr_old() : " + b +"_build_clr_new(), 0),")
                else:
                    file.write("\n\t\t\t\tSTORE_TEMP(" + b +"_build_clr_new(), 0),")   
                # Fence Colours
                if 'fence' in list(buildings[b]['childsprites'].keys()):
                    if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                        file.write("\n\t\t\t\tSTORE_TEMP(" + b + "_fence_clr(), 2),")
                # Tree Seasonality
                if 'seasonal' in buildings[b]['childsprites']['trees']['conditions']:
                    file.write("\n\t\t\t\tSTORE_TEMP(Season(), 3),")
                # Snow and switch closeout
                file.write("\n\t\t\t\tterrain_type == TILETYPE_SNOW]) ")
                file.write("\n\t\t\t\t{1: sprlay_" + b + "_" + v + "_" + l + "_snow; sprlay_" + b + "_" + v + "_" + l + "_norm; }")
            file.write("\n")

        if len(levels) > 1:
            file.write("\n\t// Level Selection")
            file.write("\n\t\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, getbits(random_bits, " + str(level_start_point) + ", " + str(BitsRequired(len(levels))) + ")) {")
            # Line for each level
            i = 0
            for l in levels:
                if i == len(levels) - 1:
                    file.write("\n\t\t\t\tswitch_" + b + "_" + v + "_" + l + "_sprites;")
                else:
                    file.write("\n\t\t\t" + str(i) + ":\tswitch_" + b + "_" + v + "_" + l + "_sprites;")
                i = i + 1
            file.write("\n\t\t}\n")

        if variants == ['a','b']:
            file.write("\n\t// Variant Selection for " + str(variants) + " using SpriteDirectionsAB()")
            file.write("\n\t"+ SpriteDirectionsAB(b))