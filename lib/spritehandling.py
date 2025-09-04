
from lib.functions import LoadJSON as LoadJSON
from lib.functions import BitsRequired as BitsRequired
from lib.functions import GetPointsBravo as GetPointsBravo
from lib.functions import SpriteDirectionsAB as SpriteDirectionsAB
from lib.functions import SpriteDirectionsABS as SpriteDirectionsABS
from lib.functions import SpriteDirectionsABENSW as SpriteDirectionsABENSW
from lib.functions import GetPointsComboLevels as GetPointsComboLevels
from lib.functions import GetPointsLevels as GetPointsLevels

buildingsJSON = 'lib/buildings.json'
recolourJSON = 'lib/recolour.json'

recolour = LoadJSON(recolourJSON)
buildings = LoadJSON(buildingsJSON)

direction_removals = {'n': 'no_north','s': 'no_south','e': 'no_east','w': 'no_west'}

def SpriteHandling(b,building_file,variants,levels,childsprites=None):
    with open(building_file, 'a') as file:
        
        # Spritelayouts
        file.write("\n" + "// Spritelayouts\n")
        climates = ['norm', 'snow']

        for v in variants:
            file.write(f"\n\t// {v.upper()} variant")
            for l in levels:
                file.write(f"\n\t\t// {l.upper()} level")
                for k in climates:
                    file.write(f"\n\t\t\t// {k.capitalize()}")
                    file.write(f"\n\t\t\t\tspritelayout sprlay_{b}_{v}_{l}_{k} {{")
                    file.write("\n\t\t\t\t\tground {\n\t\t\t\t\t\tsprite:")
                    
                    # GROUND
                    # Ground graphics incl overrides
                    if 'ground' in buildings[b].keys():
                        # Overrides
                        if 'override' in buildings[b]['ground'].keys():
                            if '[level]' in buildings[b]["ground"]["override"]:
                                level_override = buildings[b]["ground"]["override"]
                                level_override = level_override.replace("[level]",l)
                                file.write(f"{level_override}_{k}")
                            else:
                                file.write(f"{buildings[b]['ground']['override']}_{k};")
                        else:
                            file.write(f"spr_{buildings[b]['folder']}_{v}_ground_{k}")
                    else:
                        file.write(f"spr_{buildings[b]['folder']}_{v}_ground_{k}")

                    # Ground Construction State
                    if 'ground' in list(buildings[b].keys()):
                        if 'road_aware' in list(buildings[b]['ground'].keys()):
                            file.write("(LOAD_TEMP(8));")
                    else:
                        try:
                            file.write(f" ({buildings[b]['variants'][v]['construction_state']});")
                        except:
                            file.write(" (construction_state);")
                    file.write(f"\n\t\t\t\t\t}}")

                    # BUILDING
                    # Building Sprites
                    try:
                        if b in [x for x in buildings if buildings[b]["shared_gfx"] == True]:
                            file.write(f"\n\t\t\t\t\tbuilding {{\n\t\t\t\t\t\tsprite: spr_{b}_{l}_{k}")
                    except:    
                        file.write(f"\n\t\t\t\t\tbuilding {{\n\t\t\t\t\t\tsprite: spr_{b}_{v}_{l}_{k}")
                    # Buildings Constructiion State
                    try:
                        file.write(f" ({buildings[b]['variants'][v]['construction_state']});")
                    except:
                        file.write(" (construction_state);")
                    # Colour Remapping
                    file.write("\n\t\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;")
                    file.write("\n\t\t\t\t\t\tpalette: recolour_remap + LOAD_TEMP(0);")
                    # Hide Sprite Check
                    try: 
                        file.write("\n\t\t\t\t\t\thide_sprite: " + str(buildings[b]["variants"][v]["hide_sprite"]) + ";")
                    except:
                        pass
                    # X Offset Check
                    try: 
                        file.write("\n\t\t\t\t\t\t\txoffset: " + str(buildings[b]["variants"][v]["xoffset"]) + ";")
                    except:
                        pass
                    # Y Offset Check
                    try: 
                        file.write("\n\t\t\t\t\t\t\tyoffset: " + str(buildings[b]["variants"][v]["yoffset"]) + ";")
                    except:
                        pass
                    file.write(f"\n\t\t\t\t\t}}")
                    
                    # CHILDSPRITES
                    # Childsprites
                    if 'childsprites' in list(buildings[b].keys()):
                        for c in childsprites:
                            conditions = list(buildings[b]["childsprites"][c]["conditions"])
                            dontcloseout = 0
                            noconstructionstates = 0
                            
                            if 'norm_only' not in conditions or ('norm_only' in conditions and k == 'norm'):

                                # Childsprite graphics
                                if '2x2' in conditions:
                                    file.write(f"\n\t\t\t\t\tchildsprite {{ // {c}\n\t\t\t\t\t\tsprite: ")
                                    file.write(f"spr_{b}_{l}_{c}")
                                    if 'single_climate' not in conditions:
                                        file.write("_" + k)
                                elif direction_removals.get(v) in conditions:
                                    file.write(f"\n\t\t\t\t\t// No Childsprite for {c} for {v}")
                                elif 'level_driven' in conditions:
                                    if direction_removals.get(v) not in list(buildings[b]['childsprites'][c]['level'][l]):
                                        file.write(f"\n\t\t\t\t\tchildsprite {{ // {c}\n\t\t\t\t\t\tsprite: ")
                                        file.write(f"spr_{b}_{v}_{l}_{c}")
                                        if 'single_climate' not in conditions:
                                            file.write(f"_{k}")
                                    else:
                                        dontcloseout += 1
                                        noconstructionstates += 1
                                elif 'levels_share' in conditions:
                                    file.write(f"\n\t\t\t\t\tchildsprite {{ // {c}\n\t\t\t\t\t\tsprite: ")
                                    file.write(f"spr_{buildings[b]['folder']}_{v}_{c}")
                                    if 'single_climate' not in conditions:
                                        file.write("_" + k)
                                else:
                                    file.write(f"\n\t\t\t\t\tchildsprite {{ // {c}\n\t\t\t\t\t\tsprite: ")
                                    file.write(f"spr_{b}_{v}_{l}_{c}")
                                    if 'single_climate' not in conditions:
                                        file.write(f"_{k}")

                                # Childsprite Construction States
                                if '3only' in conditions:
                                    file.write(" (3); // Three only condition")
                                elif 'single' in conditions:  # If just the one, match what the building does
                                    try:
                                        file.write(" (" + str(buildings[b]["variants"][v]["construction_state"]) + "); // Same as building")
                                    except:
                                        file.write(" (construction_state); // Same as building")
                                elif 'seasonal' in conditions:
                                    if direction_removals.get(v) in conditions:
                                        file.write(f"No construction states either")
                                    elif noconstructionstates > 0:
                                        noconstructionstates += 1
                                    else:
                                        # Norm or Snow?
                                        if k == 'norm':
                                            file.write(" (LOAD_TEMP(3)); // Seasonal")
                                        else:
                                            file.write(" (3); // Seasonal, but winter tree in the snow")
                                elif '2x2' in conditions:
                                    variant_mapping = {'w':0,'s':1,'e':2,'n':3}
                                    file.write(" ("+ str(variant_mapping[v]) +");")
                                elif direction_removals.get(v) in conditions:
                                    file.write(" and no construction state either")
                                elif '4choices' in conditions:
                                    if c == 'roofs':
                                        file.write(f" (LOAD_TEMP(5));")
                                    else:
                                        print("loose end @ 4choices in Childsprite Construction States")
                                else:
                                    print("Loose End @ Childsprite Construction States")
                                
                                # Childsprite Recolouring
                                if 'remap' in conditions:
                                    if c == 'fence':
                                        file.write("\n\t\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;\n\t\t\t\t\t\tpalette: recolour_remap + LOAD_TEMP(2);")
                                    elif c == 'roofs':
                                        file.write("\n\t\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;\n\t\t\t\t\t\tpalette: recolour_remap + LOAD_TEMP(4);")
                                    elif c == 'signs':
                                        file.write("\n\t\t\t\t\t\trecolour_mode: RECOLOUR_REMAP;\n\t\t\t\t\t\tpalette: recolour_remap + LOAD_TEMP(6);")
                                    else:
                                        print(f"❌ Unclosed loop in childsprites recolouring for building {b}")
                                # End the childsprites
                                if (direction_removals.get(v) not in conditions) and (dontcloseout == 0):
                                    file.write(f"\n\t\t\t\t\t}}")
                    
                    # End the Spritelayout            
                    file.write(f"\n\t\t\t\t}}\n")

        # Getbits resolving
        colour_profiles = [b for b in list(buildings[b]["colours"].keys()) if b not in ['recolour', 'basis', 'old_era_end']]
        colour_dict = {}
        for p in colour_profiles:
            sum_prob = 0
            count = 0
            sum_prob += sum(buildings[b]["colours"][p].values())
            count += len(buildings[b]["colours"][p])
            colour_dict[p] = {'sum_prob': sum_prob, 'count': count}

        file.write("\n/*\n==================\nGetbits Allocation\n==================")

        # Are there childsprites?
        if 'childsprites' in list(buildings[b].keys()):
            file.write("\nChildsprites: " + str(childsprites)+"\n")
        else:
            file.write("\nChildsprites: 🚫\n")
        
        # What is the colour profile situation?
        file.write("\nColour Profiles: " + str(colour_dict))

        for p in colour_profiles:
            if colour_dict[p]['sum_prob'] in [2,4,8,16]:
                if buildings[b]['colours']['basis'] == 'standard':
                    if p == 'old':
                        if colour_dict['old']['sum_prob'] == colour_dict['new']['sum_prob']:
                            file.write("\n\t✅ " + p + " colour profile has " + str(colour_dict[p]['count']) + " unique colours, with probabilities summing to " + str(colour_dict[p]['sum_prob']))
                        else:
                            file.write("\n\t❌ old colour profile probability total of " + str(colour_dict['old']['count']) + " does not equal new colour total of " + str(colour_dict['new']['sum_prob']))
                    else:
                        file.write("\n\t✅ " + p + " colour profile has " + str(colour_dict[p]['count']) + " unique colours, with probabilities summing to " + str(colour_dict[p]['sum_prob']))
                elif buildings[b]['colours']['basis'] == 'levels':
                    first_level = buildings[b]['levels'][0]
                    for l in list(buildings[b]['levels']):
                        if colour_dict[l]['sum_prob'] != colour_dict[first_level]['sum_prob']:
                            file.write("\n\t❌ Sum of level probabilities does not equal")
                            print("❌ Sum of level probabilities does not equal for " + b)
                else:
                    print("❌ Slipping through the cracks at colour profiles!!")
            else:
                file.write("\n\t❌ " + b + " colour profile has " + str(colour_dict[p]['count']) + " unique colours, with probabilities summing to " + str(colour_dict[p]['sum_prob']))

        file.write("\n\nFeature\t\tNum\t\tStart\tBits\tStorage\n------------------------------------------------------------------")
        start_point = 0
        # Levels
        if len(levels) > 1:
            file.write("\nLevels\t\t" + str(len(levels)) + "\t\t" + str(start_point) + "\t\t" + str(BitsRequired(len(levels))) + "\t\t🚫")
            level_start_point = start_point
            #start_point += BitsRequired(len(levels))
            start_point += 1
        
        # Building Colours
        if buildings[b]['colours']['basis'] == 'standard':
            if colour_dict['new']['sum_prob'] > 0:
                file.write("\nBuilding\t" + str(colour_dict['new']['sum_prob']) + "\t\t" + str(start_point) + "\t\t" + str(BitsRequired(colour_dict['new']['sum_prob'])) + "\t\tLOAD_TEMP(0)" )
                building_colour_start_point = start_point
                #start_point = start_point + BitsRequired(colour_dict['new']['sum_prob'])
                start_point += 1
        elif buildings[b]['colours']['basis'] == 'levels':
            if colour_dict[first_level]['sum_prob'] > 0:
                file.write("\nBuilding\t" + str(colour_dict[first_level]['sum_prob']) + "\t\t" + str(start_point) + "\t\t" + str(BitsRequired(colour_dict[first_level]['sum_prob'])) + "\t\tLOAD_TEMP(0)" )
                building_colour_start_point = start_point
                #start_point = start_point + BitsRequired(colour_dict[first_level]['sum_prob'])
                start_point += 1
        else:
            print("❌ Unclosed loop for " + b)

        # Childsprites
        if childsprites != None:
        
            # Fence Colours
            if 'fence' in list(buildings[b]['childsprites'].keys()):
                if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                    file.write("\nFence 🎨\t" + str(4) + "\t\t" + str(start_point) + "\t\t" + str(2) + "\t\tLOAD_TEMP(2)")
                    fence_colour_start_point = start_point
                    start_point += 1
                
            # Roof 
            if 'roofs' in list(buildings[b]['childsprites'].keys()):
                # Roof Colours
                if 'remap' in buildings[b]['childsprites']['roofs']['conditions']:
                    file.write(f"\nRoof 🎨\t\t{colour_dict['new']['sum_prob']}\t\t{start_point}\t\t{BitsRequired(colour_dict['roofs_new']['sum_prob'])}\t\tLOAD_TEMP(4)")
                    roofs_colour_start_point = start_point
                    start_point += 1

                # Roof Variations
                if '4choices' in buildings[b]['childsprites']['roofs']['conditions']:
                    file.write(f"\nRoof Var\t{4}\t\t{start_point}\t\t{2}\t\tLOAD_TEMP(5)")
                    roofs_variations_start_point = start_point
                    start_point += 1

            # Sign Colours
            if 'signs' in list(buildings[b]['childsprites'].keys()):
                if 'remap' in buildings[b]['childsprites']['signs']['conditions']:
                    file.write(f"\nSigns 🎨\t{4}\t\t{start_point}\t\t{2}\t\tLOAD_TEMP(6)")
                    signs_colour_start_point = start_point
                    start_point += 1

        file.write("\n*/\n")

        # RANDOM SWITCHES
        file.write("\n// Random Switches")
        
        # Building Colours
        file.write("\n\t// Building Colours")
        building_colour_profiles = [p for p in colour_profiles if p not in ['fence','trees','roofs_new','roofs_old','signs']]
        for p in building_colour_profiles:
            file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, {b}_build_clr_{p}, getbits(random_bits, {building_colour_start_point}, {BitsRequired(colour_dict[p]['sum_prob'])})) {{")
            points = GetPointsBravo(buildings,b,p)
            i = 0
            for c in list(buildings[b]['colours'][p].keys()):
                if i == len(list(buildings[b]['colours'][p].keys())) - 1:
                    file.write(f"\n\t\t\t\treturn {recolour[c]['remap']};")
                else:
                    file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
                i = i + 1
            file.write("\n\t\t}")

        # Childsprites
        if childsprites != None:

            # Fence Colours
            if 'fence' in childsprites:
                if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                    file.write("\n\t// Fence Colours")
                    file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, {b}_fence_clr, getbits(random_bits, {fence_colour_start_point}, {2})) {{")
                    points = GetPointsBravo(buildings,b,"fence")
                    i = 0
                    for c in list(buildings[b]['colours']['fence'].keys()):
                        if i == len(list(buildings[b]['colours']['fence'].keys())) - 1:
                            file.write("\n\t\t\t\treturn " + str(recolour[c]['remap']) + ";")
                        else:
                            file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
                        i = i + 1
                    file.write("\n\t\t}")

            # Roofs
            if 'roofs' in childsprites:
                # Colours
                if 'remap' in buildings[b]['childsprites']['roofs']['conditions']:
                    file.write("\n\t// Roof Colours")
                    roof_colour_profiles = [item for item in buildings[b]['colours'] if "roofs" in item]
                    for rcp in roof_colour_profiles:
                        file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, {b}_{rcp}, getbits(random_bits, {roofs_colour_start_point}, {BitsRequired(colour_dict[rcp]['sum_prob'])})) {{")
                        points = GetPointsBravo(buildings,b,rcp)
                        i = 0
                        for c in list(buildings[b]['colours'][rcp].keys()):
                            if i == len(list(buildings[b]['colours'][rcp].keys())) - 1:
                                file.write("\n\t\t\t\treturn " + str(recolour[c]['remap']) + ";")
                            else:
                                file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
                            i = i + 1
                        file.write("\n\t\t}")

            # Sign Colours
            if 'signs' in childsprites:
                if 'remap' in buildings[b]['childsprites']['signs']['conditions']:
                    file.write("\n\t// Sign Colours")
                    file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, {b}_signs_clr, getbits(random_bits, {signs_colour_start_point}, {2})) {{")
                    points = GetPointsBravo(buildings,b,"signs")
                    i = 0
                    for c in list(buildings[b]['colours']['signs'].keys()):
                        if i == len(list(buildings[b]['colours']['signs'].keys())) - 1:
                            file.write("\n\t\t\t\treturn " + str(recolour[c]['remap']) + ";")
                        else:
                            file.write("\n\t\t\t" + points[i] + ":\treturn " + str(recolour[c]['remap']) + ";")
                        i = i + 1
                    file.write("\n\t\t}")

        # SPRITELAYOUT SWITCH
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
                if buildings[b]['colours']['basis'] == 'standard':
                    if 'old_era_end' in buildings[b]['colours']:
                        file.write(f"\n\t\t\t\tSTORE_TEMP((current_year - age) < {buildings[b]['colours']['old_era_end']} ? {b}_build_clr_old() : {b}_build_clr_new(), 0),")
                    else:
                        file.write("\n\t\t\t\tSTORE_TEMP(" + b +"_build_clr_new(), 0),")  
                elif buildings[b]['colours']['basis'] == 'levels':
                    file.write("\n\t\t\t\tSTORE_TEMP(" + b +"_build_clr_" + l + "(), 0),")  
                else:
                    print("❌ Unclosed loop for " + b + " at spritelayout switches")
                
                # Ground Sprites
                if 'ground' in list(buildings[b].keys()):
                    if 'road_aware' in list(buildings[b]['ground'].keys()):
                        file.write(f"\n\t\t\t\tSTORE_TEMP(GroundRoadAware(), 8),")

                # Childsprites
                if childsprites != None:
                    # Fence Colours
                    if 'fence' in list(buildings[b]['childsprites'].keys()):
                        if 'remap' in buildings[b]['childsprites']['fence']['conditions']:
                            file.write("\n\t\t\t\tSTORE_TEMP(" + b + "_fence_clr(), 2),")
                    # Roof
                    if 'roofs' in list(buildings[b]['childsprites'].keys()):
                        # Roof Colours
                        if 'remap' in buildings[b]['childsprites']['roofs']['conditions']:
                            if 'old_colours' in buildings[b]['childsprites']['roofs']['conditions']:
                                file.write(f"\n\t\t\t\tSTORE_TEMP((current_year - age) < {buildings[b]['colours']['old_era_end']} ? {b}_roofs_old() : {b}_roofs_new(), 4),")
                            else:
                                file.write(f"\n\t\t\t\tSTORE_TEMP({b}_roofs_new(), 4),")
                        # Roof Variants
                        if '4choices' in buildings[b]['childsprites']['roofs']['conditions']:
                            file.write(f"\n\t\t\t\tSTORE_TEMP(getbits(random_bits, {roofs_variations_start_point}, {2}), 5),")
                    # Sign Colours
                    if 'signs' in list(buildings[b]['childsprites'].keys()):
                        if 'remap' in buildings[b]['childsprites']['signs']['conditions']:
                            file.write(f"\n\t\t\t\tSTORE_TEMP({b}_signs_clr(), 6),")
                    # Tree Seasonality
                    if 'trees' in list(buildings[b]['childsprites'].keys()):
                        if 'seasonal' in buildings[b]['childsprites']['trees']['conditions']:
                            file.write("\n\t\t\t\tSTORE_TEMP(Season(), 3),")
                # Snow and switch closeout
                file.write("\n\t\t\t\tterrain_type == TILETYPE_SNOW]) ")
                file.write("\n\t\t\t\t{1: sprlay_" + b + "_" + v + "_" + l + "_snow; sprlay_" + b + "_" + v + "_" + l + "_norm; }")
            file.write("\n")

        if buildings[b]['tile_size'] == 'HOUSE_SIZE_1X1':
            if len(levels) > 1:
                file.write("\n\t// Level Selection")
                for v in variants:
                    if len(variants) > 1:
                        file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, switch_{b}_{v}_sprites, getbits(random_bits, {level_start_point}, {BitsRequired(len(levels))})) {{")
                    else:
                        file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, switch_{b}_sprites, getbits(random_bits, {level_start_point}, {BitsRequired(len(levels))})) {{")
                    # Line for each level
                    i = 0
                    for l in levels:
                        if i == len(levels) - 1:
                            file.write(f"\n\t\t\t\tswitch_{b}_{v}_{l}_sprites;")
                        else:
                            file.write(f"\n\t\t\t{i}:\tswitch_{b}_{v}_{l}_sprites;")
                        i = i + 1
                    file.write("\n\t\t}\n")
        elif buildings[b]['tile_size'] == 'HOUSE_SIZE_2X2':
            if len(levels) > 1:
                file.write("\n\t// Level Selection")
                for v in variants:
                    file.write("\n\t\tswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v +"_sprites, getbits(random_bits, " + str(level_start_point) + ", " + str(BitsRequired(len(levels))) + ")) {")
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
            file.write(f"\n\t// Variant Selection for {variants} using SpriteDirectionsAB()")
            file.write("\n\t"+ SpriteDirectionsAB(b))
        elif variants == ['a','b','s']:
            file.write(f"\n\t// Variant Selection for {variants} using SpriteDirectionsABS()")
            file.write("\n\t"+ SpriteDirectionsABS(b))
        elif variants == ['a','b','e','n','s','w']:
            file.write(f"\n\t// Variant Selection for {variants} using SpriteDirectionsABENSW()")
            file.write("\n\t" + SpriteDirectionsABENSW(b))

        # NAME SWITCHES
        if 'name' in buildings[b]["graphics"].keys():
            file.write("\n// Name Switches")

            # Standard Colouring basis
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
            
            # Different colouring for each level
            elif buildings[b]["colours"]["basis"] == 'levels':
                colour_options = [b for b in list(buildings[b]["colours"].keys()) if b not in ['recolour', 'basis', 'old_era_end']]
                all_colours = []
                for o in colour_options:
                    all_colours = (list(buildings[b]["colours"][o].values()) + all_colours)
                # Write Switch Header
                file.write(f"\n\t\tswitch (FEAT_HOUSES, SELF, switch_{b}_name, getbits(random_bits, {level_start_point}, {BitsRequired(len(levels))}) ){{")
                points = GetPointsComboLevels(buildings,b,all_colours)
                i = 0
                for l in levels:
                    if i == len(levels) - 1:
                        file.write(f"\n\t\t\t\t{buildings[b]['graphics']['name']['names'][l]};\t// {l}")
                    else:
                        file.write(f"\n\t\t\t{i}:\t{buildings[b]['graphics']['name']['names'][l]};\t// {l}")
                        i = i + 1
                file.write("\n\t}\n") 
            else: 
                print("Name Switches: Basis not found!")