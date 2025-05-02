
import json
from itertools import accumulate

buildingsJSON = 'lib/new_buildings.json'
recolourJSON = 'lib/recolour.json'

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

recolour = LoadJSON(recolourJSON)
buildings = LoadJSON(buildingsJSON)

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

def CreateBuildingFiles():
    newjsonbuildings = [x for x in buildings if buildings[x]["newjson"] == True ]

    # Create Building PNML File
    for b in newjsonbuildings:
        with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'w') as file:
            file.write("\n" + "// " + b + "\n")
            if buildings[b]["folder"] == b:
                file.write('\n#include "src/houses/' + b + '/gfx/' + b + '_sprites.pnml"\n')
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
                            # Ground Override
                            try:
                                file.write("\n\t\t\t\t\t\tsprite: " + buildings[b]["ground_override"] + "_" + k)
                            except:
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
                    if b == buildings[b]["folder"]:
                        for v in buildings[b]["variants"]:
                            file.write("\n\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_sprites, current_year - age) {\n\t\t0.." + str(buildings[b]["end_of_old_era"]) + ": switch_" + b + "_" + v + "_old;\n\t\tswitch_" + b + "_" + v + "_all;\n\t}")
                    else:
                        for v in buildings[b]["variants"]:
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
