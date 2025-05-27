
import json
from itertools import accumulate
from lib.functions import LoadJSON as LoadJSON
from lib.functions import NumLevels as NumLevels
from lib.functions import GetPoints as GetPoints
from lib.functions import GetPointsComboLevels as GetPointsComboLevels
from lib.functions import GetPointsLevels as GetPointsLevels
from lib.functions import SpriteDirectionsAB as SpriteDirectionsAB
from lib.functions import SpriteDirectionsABENSW as SpriteDirectionsABENSW
from lib.functions import SpriteDirectionsABS as SpriteDirectionsABS

buildingsJSON = 'lib/buildings.json'
recolourJSON = 'lib/recolour.json'

recolour = LoadJSON(recolourJSON)
buildings = LoadJSON(buildingsJSON)

def CreateBuildingFiles():
    
    with open(r'./lib/buildingfileslog.txt', 'w') as log:
        
        # Overall
        log.write('OVERALL STATS')
        manual_switchers = [b for b in buildings if 'manual' in list(buildings[b].keys())]
        log.write('\nmanual switchers = ' + str(manual_switchers))
        non_standard_colour_basis = [b for b in buildings if buildings[b]["colours"]["basis"] != 'standard']
        log.write('\ncolour basis exceptions = ' + str(non_standard_colour_basis))
        recolour_buildings = [b for b in buildings if buildings[b]["colours"]["recolour"] == True]
        name_switchers = [b for b in buildings if 'name' in buildings[b]["graphics"].keys()]
        log.write('\nname switchers = ' + str(name_switchers))

        # Building by Building
        log.write('\n\nBUILDINGS')
        for b in buildings:
            with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'w') as file:
                log.write('\n\n' + b + ' opening')
                log.write('\n\tBUILDING DEFINITIONS')
                # Variants
                variants = list(buildings[b]["variants"].keys())
                log.write('\n\t\tVariants:\t\t\t' + str(variants))
                # Levels
                levels = list(buildings[b]["levels"])
                log.write('\n\t\tLevels:\t\t\t\t' + str(levels))
                # Colour Profiles, e.g. 'new', 'old', ...
                colour_profile = [b for b in list(buildings[b]["colours"].keys()) if b not in ['recolour', 'basis', 'old_era_end']]
                log.write('\n\t\tColour Profiles:\t' + str(colour_profile))
                # All Unique Colours
                all_colours = []
                for o in colour_profile:
                    all_colours = list(set(list(buildings[b]["colours"][o].keys()) + all_colours))
                    all_colours.sort()
                log.write('\n\t\tAll Unique Colours:\t' + str(all_colours))
                # Updated All Colours
                if b in non_standard_colour_basis:
                    for l in levels:
                        updated_all_colours =  list(set(list(buildings[b]["colours"][l].keys())))
                        log.write('\n\t\tUpdated All Colours:\t' + l + ':\t' +str(updated_all_colours))
                else:
                    updated_all_colours =  all_colours 

                # CREATE A FILE
                file.write("\n" + "// " + b + "\n")
                # Bring in Sprite pnmls if needed
                if buildings[b]["folder"] == b:
                    file.write('\n#include "src/houses/' + b + '/gfx/' + b + '_sprites.pnml"\n')
                # Manual Switchers
                if 'manual' in buildings[b].keys():
                    log.write('\n\tManual sprites added for ' + b)
                    file.write('\n#include "src/houses/' + buildings[b]["folder"] + '/' + b + '_manual_switches.pnml"\n')
                # Non Manual Switchers
                else:
                    log.write('\n\tSPRITELAYOUTS')
                    climates = ["norm","snow"]
                    file.write("\n// Spritelayouts")
                    for v in variants:
                        file.write("\n\t// " + v)
                        for l in levels:
                            file.write("\n\t\t// " + l)  
                            if b in non_standard_colour_basis:
                                updated_all_colours =  list(set(list(buildings[b]["colours"][l].keys())))  
                            for c in updated_all_colours:
                                file.write("\n\t\t\t// " + c)
                                for k in climates:
                                    file.write("\n\t\t\t\t// " + k)
                                    # Spritelayout Header
                                    file.write("\n\t\t\t\tspritelayout sprlay_" + b + "_" + v + "_" + l + "_" + c + "_" + k + " {\n\t\t\t\t\tground {")
                                    # Ground Override
                                    if 'ground_override' in buildings[b].keys():
                                        if '[level]' in buildings[b]["ground_override"]:
                                            level_override = buildings[b]["ground_override"]
                                            level_override = level_override.replace("[level]",l)
                                            file.write("\n\t\t\t\t\t\tsprite: " + level_override + "_" + k)
                                        else:
                                            file.write("\n\t\t\t\t\t\tsprite: " + buildings[b]["ground_override"] + "_" + k)
                                    else:
                                        file.write("\n\t\t\t\t\t\tsprite: spr_" + buildings[b]["folder"] + "_" + v + "_ground_" + k)
                                    # Ground Construction State
                                    try:
                                        file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                                    except:
                                        file.write(" (construction_state);")
                                    # Building Sprites
                                    try:
                                        if b in [x for x in buildings if buildings[b]["shared_gfx"] == True]:
                                            file.write("\n\t\t\t\t\t}\n\t\t\t\t\tbuilding {\n\t\t\t\t\t\tsprite: spr_" + b + "_" + l +"_" + k)
                                    except:    
                                        file.write("\n\t\t\t\t\t}\n\t\t\t\t\tbuilding {\n\t\t\t\t\t\tsprite: spr_" + b + "_" + v + "_" + l +"_" + k)
                                    # Buildings Constructiion State
                                    try:
                                        file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                                    except:
                                        file.write(" (construction_state);")
                                    # Colour Remapping
                                    file.write("\n\t\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;")
                                    file.write("\n\t\t\t\t\t\tpalette: recolour_remap + " + str(recolour[c]["remap"]) + ";")
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
                                    # Childsprite
                                    if 'childsprite' in list(buildings[b].keys()):
                                        file.write("\n\t\t\t\t\tchildsprite {")
                                        if buildings[b]["childsprite"]["basis"] == 'levels':
                                            if 'shared_gfx' in list(buildings[b].keys()):
                                                file.write("\n\t\t\t\t\t\tsprite: spr_" + b + "_" + l + "_" + buildings[b]["childsprite"]["position"] + "_" + k)
                                            else:
                                                file.write("\n\t\t\t\t\t\tsprite: spr_" + b + "_" + v + "_" + l + "_" + buildings[b]["childsprite"]["position"] + "_" + k)
                                        try: 
                                            file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + ");")
                                        except:
                                            file.write(" (construction_state);")
                                        file.write("\n\t\t\t\t\t}")
                                    file.write("\n\t\t\t}\n")
                                file.write("\n\t\t\t\tswitch(FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + l + "_" + c + "_snow, terrain_type) {\n\t\t\t\t\tTILETYPE_SNOW: sprlay_" + b + "_" + v + "_" + l + "_" + c + "_snow;\n\t\t\t\t\tsprlay_" + b + "_" + v + "_" + l + "_" + c + "_norm;\n\t\t\t\t}\n")
                    file.write("\n")

                    # COLOUR SWITCHES
                    if b in recolour_buildings:
                        file.write("\n// Colour Switches")
                        # First check what's the colour option -standard, or something else?
                        if buildings[b]["colours"]["basis"] == 'standard':
                            # When standard, is there also an old era?
                            if "old_era_end" in buildings[b]["colours"].keys(): 
                                colour_options = ["new","old"]   
                            else:
                                colour_options = ["sprites"]
                            for v in buildings[b]["variants"]:
                                for o in colour_options:
                                    if o == "new" or o =="sprites": # When colour option is 'new' or 'sprites'
                                        points = GetPoints(buildings,b,"new")
                                        # Switch header
                                        keys = list(buildings[b]["variants"].keys())
                                        if "old_era_end" in buildings[b]["colours"].keys() or keys == ['a', 'b'] or keys == ['a', 'b', 'e', 'n', 's', 'w'] or keys == ['n', 'e', 'w', 's'] or keys == ['n', 'w'] or keys == ['n', 'e'] or keys == ['a', 'b', 's']:
                                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + o + ", random_bits % " + str(len(buildings[b]["levels"]) * sum(buildings[b]["colours"]["new"].values())) + " ) { ")
                                        else:
                                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + o + ", random_bits % " + str(len(buildings[b]["levels"]) * sum(buildings[b]["colours"]["new"].values())) + " ) { ")
                                        # Each line in switch
                                        i = 0
                                        for l in buildings[b]["levels"]:
                                            for c in buildings[b]["colours"]["new"]:
                                                file.write("\n\t\t" + points[i] + ":\tswitch_" + b + "_" + v + "_" + l +"_" + c + "_snow;")
                                                i = i + 1
                                    else: # When colour option is 'old'
                                        points = GetPoints(buildings,b,"old")
                                        file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + o + ", random_bits % " + str(len(buildings[b]["levels"]) * sum(buildings[b]["colours"]["old"].values())) + " ) { ")
                                        i = 0
                                        for l in buildings[b]["levels"]:
                                            for c in buildings[b]["colours"]["old"]:
                                                file.write("\n\t\t" + points[i] +":\tswitch_" + b + "_" + v + "_" + l +"_" + c + "_snow;")
                                                i = i + 1
                                    file.write("\n\t}")     
                            # Switches for New vs Old 
                            if "old_era_end" in buildings[b]["colours"].keys():
                                if b == buildings[b]["folder"]:
                                    for v in buildings[b]["variants"]:
                                        file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, current_year - age) {\n\t\t0.." + str(buildings[b]["colours"]["old_era_end"]) + ": switch_" + b + "_" + v + "_old;\n\t\tswitch_" + b + "_" + v + "_new;\n\t}")
                                else:
                                    for v in buildings[b]["variants"]:
                                        if v == 'h':
                                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, current_year - age) {\n\t\t0.." + str(buildings[b]["colours"]["old_era_end"]) + ": switch_" + b + "_" + v + "_old;\n\t\tswitch_" + b + "_" + v + "_new;\n\t}")
                                        else:
                                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_sprites, current_year - age) {\n\t\t0.." + str(buildings[b]["colours"]["old_era_end"]) + ": switch_" + b + "_" + v + "_old;\n\t\tswitch_" + b + "_" + v + "_new;\n\t}")
                        
                        # Non-Standard - When there are different colour options per level
                        elif buildings[b]["colours"]["basis"] == 'levels':
                            level_options = list(buildings[b]["levels"])
                            colour_options = [b for b in list(buildings[b]["colours"].keys()) if b not in ['recolour', 'basis', 'old_era_end']]
                            all_colours = []
                            for o in colour_options:
                                all_colours = (list(buildings[b]["colours"][o].values()) + all_colours)
                            for v in buildings[b]["variants"]:
                                # Write the switch header
                                file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_sprites, random_bits % " + str(sum(all_colours)) + " ) { ")
                                # Then for each line, loop through the levels, and it's colour options
                                i = 0
                                points = GetPointsComboLevels(buildings,b,all_colours)
                                for l in level_options:
                                    keys = list(buildings[b]["variants"].keys())
                                    for c in buildings[b]["colours"][l]:
                                        file.write("\n\t\t" + points[i] + ":\tswitch_" + b + "_" + v + "_" + l +"_" + c + "_snow;")
                                        i = i + 1
                                file.write("\n\t}")  
                        else:
                            pass #print("Check here #001 - " + b)
                        file.write("\n")
                    else:
                        print("Check here #002 - " + b)  
                    
                    # DIRECTION SWITCHES
                    # For A and B variants
                    if variants == ["a", "b"]:
                        file.write("\n// Direction Switches")
                        file.write("\n\t"+ SpriteDirectionsAB(b))
                    # For A, B, E, N, S and W variants
                    if variants == ["a", "b", "e", "n", "s", "w"]:
                        file.write("\n// Direction Switches")
                        file.write("\n\t"+ SpriteDirectionsABENSW(b))
                    # For A, B and S variants
                    if variants == ["a", "b", "s"]:
                        file.write("\n// Direction Switches")
                        file.write("\n\t"+ SpriteDirectionsABS(b))

                    # NAME SWITCHES
                    if b in name_switchers:
                        log.write("\n\t\tName Switcher")
                        file.write("\n// Name Switches")
                        if buildings[b]["colours"]["basis"] == 'standard':
                            if buildings[b]["graphics"]["name"]["convention"] == 'levels':
                                file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_name, random_bits % " + str(len(buildings[b]["levels"]) * sum(buildings[b]["colours"]["new"].values())) + " ) { ")
                                points = GetPointsLevels(buildings,b,"new")
                                i = 0
                                for level in buildings[b]["levels"]:
                                    file.write("\n\t\t" + points[i])
                                    file.write("\t" + buildings[b]["graphics"]["name"]["names"][level] + ";")
                                    i = i + 1
                                file.write("\n\t}\n")
                        elif buildings[b]["colours"]["basis"] == 'levels':
                            colour_options = [b for b in list(buildings[b]["colours"].keys()) if b not in ['recolour', 'basis', 'old_era_end']]
                            all_colours = []
                            for o in colour_options:
                                all_colours = (list(buildings[b]["colours"][o].values()) + all_colours)
                            # Write Switch Header
                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_name, random_bits % " + str(sum(all_colours)) + " ) { ")
                            points = GetPointsComboLevels(buildings,b,all_colours)
                            i = 0
                            for l in level_options:
                                for c in buildings[b]["colours"][l]:
                                    file.write("\n\t\t" + points[i] + ":\t" + buildings[b]["graphics"]["name"]["names"][l] + ";")
                                    i = i + 1
                            file.write("\n\t}\n") 
                        else: 
                            print("Name Switches: Basis not found!")

                # ITEM BLOCK
                log.write("\n\tITEM BLOCK")

                # Parameter if needed
                if 'parameter'in buildings[b].keys():
                    file.write("\n" + buildings[b]["parameter"])
                # Item Block Header
                file.write("\n// Item Block\n\titem(FEAT_HOUSES, item_" + b + ", " + str(buildings[b]["id"]) + ", " + str(buildings[b]["tile_size"])  + "){")
                # Properties Block
                file.write("\n\t\tproperty {")
                file.write("\n\t\t\tsubstitute:\t\t\t\t\t" +        str(buildings[b]["properties"]["substitute"]) + ";")
                if b not in name_switchers:
                    file.write("\n\t\t\tname:\t\t\t\t\t\t" +        str(buildings[b]["properties"]["name"]) + ";")
                file.write("\n\t\t\tpopulation:\t\t\t\t\t" +        str(buildings[b]["properties"]["population"]) + ";")
                file.write("\n\t\t\taccepted_cargos:\t\t\t" +       str(buildings[b]["properties"]["accepted_cargos"]) + ";")
                file.write("\n\t\t\tlocal_authority_impact:\t\t" +  str(buildings[b]["properties"]["local_authority_impact"]) + ";")
                file.write("\n\t\t\tremoval_cost_multiplier:\t" +   str(buildings[b]["properties"]["removal_cost_multiplier"]) + ";")
                file.write("\n\t\t\tprobability:\t\t\t\t" +         str(buildings[b]["properties"]["probability"]) + ";")
                file.write("\n\t\t\tyears_available:\t\t\t" +       str(buildings[b]["properties"]["years_available"]) + ";")
                file.write("\n\t\t\tminimum_lifetime:\t\t\t" +      str(buildings[b]["properties"]["minimum_lifetime"]) + ";")
                file.write("\n\t\t\tavailability_mask:\t\t\t" +     str(buildings[b]["properties"]["availability_mask"]) + ";")
                file.write("\n\t\t\tbuilding_class:\t\t\t\t" +      str(buildings[b]["properties"]["building_class"]) + ";")
                # Graphics Block
                file.write("\n\t\t\t}\n\t\tgraphics {")
                if 'default' in buildings[b]["graphics"].keys(): 
                    file.write("\n\t\t\tdefault:\t\t\t\t\t" +       str(buildings[b]["graphics"]["default"]) + ";")
                if 'graphics_north' in buildings[b]["graphics"].keys():  
                    file.write("\n\t\t\tgraphics_north:\t\t\t\t" +  str(buildings[b]["graphics"]["graphics_north"]) + ";")
                if 'graphics_east' in buildings[b]["graphics"].keys():  
                    file.write("\n\t\t\tgraphics_east:\t\t\t\t" +   str(buildings[b]["graphics"]["graphics_east"]) + ";")
                if 'graphics_west' in buildings[b]["graphics"].keys():   
                    file.write("\n\t\t\tgraphics_west:\t\t\t\t" +   str(buildings[b]["graphics"]["graphics_west"]) + ";")
                if 'graphics_south' in buildings[b]["graphics"].keys():   
                    file.write("\n\t\t\tgraphics_south:\t\t\t\t" +  str(buildings[b]["graphics"]["graphics_south"]) + ";")
                # Name
                if b in name_switchers:
                    file.write("\n\t\t\tname:\t\t\t\t\t\tswitch_" + b + "_name;")
                # Construction Check
                if 'construction_check' in buildings[b]["graphics"].keys():
                    file.write("\n\t\t\tconstruction_check:\t\t\t"+ str(buildings[b]["graphics"]["construction_check"]) + ";")
                # Protection Check
                if 'protection' in buildings[b]["graphics"].keys():
                    file.write("\n\t\t\tprotection:\t\t\t\t\t" +    str(buildings[b]["graphics"]["protection"]) + ";")
                file.write("\n\t\t\tcargo_production:\t\t\t" +      str(buildings[b]["graphics"]["cargo_production"]) + ";")
                # Parameter
                if 'parameter'in buildings[b].keys():
                    file.write("\n\t\t}\n\t}\n\t}\n")
                else: # Normal Item Block Closing
                    file.write("\n\t\t}\n\t}\n")

                # Final Close File (eventually)
                log.write("\n\tBuilding Completed")
                file.close()
        # Close the log
        log.close()
