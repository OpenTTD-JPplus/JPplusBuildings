
from colourprofiles import buildings_dict as buildings_dict
import copy
import itertools

buildings = list(buildings_dict.keys())

print("Running switches_colours.py")

# ########################## #
# CREATE DICTIONARIES #
# ########################## #

colour_dict = {}
colour_weightings_all_dict = {}
colour_weightings_old_dict = {}
for b in buildings:
    colours = list(buildings_dict[b]["colours"].keys())
    for c in colours:
        colour_dict[b] = buildings_dict[b]["colours"]
        colour_weightings_all_dict[b] = list(buildings_dict[b]["colours"].values())
        if buildings_dict[b]["old_colours"] == False:
            colour_weightings_old_dict[b] = False
        else:
            colour_weightings_old_dict[b] = list(buildings_dict[b]["old_colours"].values())

# Create dictionary showing what levels are available per height
heights_dict = {}
for b in buildings:
    heights = list(buildings_dict[b]["heights"])
    for h in heights:
        heights_dict[b] = (buildings_dict[b]["heights"])

# Create dictionary with number of levels per height
num_heights_dict = copy.deepcopy(heights_dict)
for b in buildings:
    heights = list(buildings_dict[b]["heights"])
    for h in heights:
        num_heights_dict[b][h] = len(num_heights_dict[b][h]) # {'fukuda': {'m': 1, 'l': 1}, 'harada': {'m': 1, 'l': 1}, 'hayashi': {'s': 2, 'm': 2}, 'hirano': {'s': 2, 'm': 2}}

# Map the colour weighting to each building and each height
colour_weightings_all_levels_dict = copy.deepcopy(colour_weightings_all_dict)
colour_weightings_old_levels_dict = copy.deepcopy(colour_weightings_old_dict)

colours_all_weightings = copy.deepcopy(num_heights_dict)
for b in buildings:
    heights = list(colours_all_weightings[b].keys())
    for h in heights:
        colours_all_weightings[b][h] = colour_weightings_all_levels_dict[b] * num_heights_dict[b][h] 

colours_old_weightings = copy.deepcopy(num_heights_dict)
for b in buildings:
    heights = list(colours_old_weightings[b].keys())
    for h in heights:
        if buildings_dict[b]["old_colours"] == False:
            colours_old_weightings[b][h] = False
        else:
            colours_old_weightings[b][h] = colour_weightings_old_levels_dict[b] * num_heights_dict[b][h] 

# Calculate the end point of the random bits
end_point_all = copy.deepcopy(colours_all_weightings)
end_point_old = copy.deepcopy(colours_old_weightings)
for b in buildings:
    heights = list(colours_all_weightings[b].keys())
    for h in heights:
        end_point_all[b][h] = list(itertools.accumulate(colours_all_weightings[b][h]))
        end_point_all[b][h] = [x - 1 for x in end_point_all[b][h]]
        if buildings_dict[b]["old_colours"] == False:
            end_point_old[b][h] = False
        else:
            end_point_old[b][h] = list(itertools.accumulate(colours_old_weightings[b][h]))
            end_point_old[b][h] = [x - 1 for x in end_point_old[b][h]]

# Calculate the start point of the random bits
start_point_all = copy.deepcopy(end_point_all)
start_point_old = copy.deepcopy(end_point_old)
for b in buildings:
    heights = list(start_point_all[b].keys())
    heights_old = list(start_point_old[b].keys())
    # For ALL colours
    for h in heights:
        bits = list(start_point_all[b][h])
        n = 0
        for g in bits:
            start_point_all[b][h][n] = end_point_all[b][h][n] - ( colours_all_weightings[b][h][n] - 1)
            n = n + 1
    # For OLD colours
    for i in heights_old:
        m = 0
        if buildings_dict[b]["old_colours"] == False:
            start_point_old[b][i] = False
            m = m + 1
        else:
            bits_old = list(start_point_old[b][i])
            for f in bits_old: 
                start_point_old[b][i][m] = end_point_old[b][i][m] - ( colours_old_weightings[b][i][m] - 1)
                m = m + 1

# Calculate the random bit range
random_bits_all_range = copy.deepcopy(end_point_all)
random_bits_old_range = copy.deepcopy(end_point_old)
for b in buildings:
    heights = list(random_bits_all_range[b].keys())
    heights_old = list(random_bits_old_range[b].keys())
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
    # For OLD colours
    for i in heights_old:
        m = 0
        if buildings_dict[b]["old_colours"] == False:
            random_bits_old_range[b][i] = False
            m = m + 1
        else:
            bits_old = list(start_point_old[b][i])
            for f in bits_old: 
                if start_point_old[b][h][m] == end_point_old[b][h][m]:
                    random_bits_old_range[b][i][m] = str(start_point_old[b][i][m])
                else:
                    random_bits_old_range[b][i][m] = str(start_point_old[b][i][m]) + ".." + str(end_point_old[b][i][m])
                m = m + 1

# Calculate the random bits totals - adj for number of levels is made later
random_bits_total_all_dict = {}
for b in buildings:
    random_bits_total_all_dict[b] = sum(buildings_dict[b]["colours"].values())

random_bits_total_old_dict = {}
for b in buildings:
    if buildings_dict[b]["old_colours"] == False:
         random_bits_total_old_dict[b] = False
    else:
        random_bits_total_old_dict[b] = sum(buildings_dict[b]["old_colours"].values())


# Add the lines for each colour option and it's random bit allocation
for b in buildings:
    # Create an initial file
    f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "w")
    f.write("\n// " + b + " ALL colours\n")
    f.close()
    variants = list(buildings_dict[b]["variants"])
    for v in variants:
        heights = list(buildings_dict[b]["heights"]) # 's', 'm', 'l' etc
        n = 0
        for h in heights:
            num_heights = len(buildings_dict[b]["heights"][h])
            # Add the switch line and update details
            f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
            # Modern Colours only
            if buildings_dict[b]["old_colours"] == False and v == 'x':
                f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 1 \n")
            elif buildings_dict[b]["old_colours"] == False and v != 'x' and (h == 'k' or h == 'c'):
                f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_" + v + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 2\n")   
            elif buildings_dict[b]["old_colours"] == False and v != 'x' and h != "k":
                f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_sprites, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 3\n")  
            #Old Colours will come latter
            elif buildings_dict[b]["old_colours"] != False and v == 'x':
                f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_modern, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 4\n")
            elif buildings_dict[b]["old_colours"] != False and v != 'x':
                f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_modern, random_bits % " + str(random_bits_total_all_dict[b] * num_heights) + " ) { // Ref 5\n")
            else:
                print("// Ref 6 - " + b + " not allocated to an option")
            
            f.close()
            levels = list(buildings_dict[b]["heights"].values())[n]
            n = n + 1
            m = 0
            for l in levels:
                colours = list(buildings_dict[b]["colours"].keys())
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
for b in buildings:
    if buildings_dict[b]["old_colours"] == False:
        pass
    else:
        f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
        f.write("\n// " + b + " OLD colours\n")
        f.close()
        variants = list(buildings_dict[b]["variants"])
        for v in variants:
            heights = list(buildings_dict[b]["heights"])
            n = 0
            for h in heights:
                num_heights = len(buildings_dict[b]["heights"][h])
                # Add the switch line and update details
                f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                if v == 'x':
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_old, random_bits % " + str(random_bits_total_old_dict[b] * num_heights) + " ) {\n")
                else:
                    f.write("\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_old, random_bits % " + str(random_bits_total_old_dict[b] * num_heights) + " ) {\n")
                f.close()
                levels = list(buildings_dict[b]["heights"].values())[n]
                n = n + 1
                m = 0
                for l in levels:
                    colours = list(buildings_dict[b]["old_colours"].keys())
                    for c in colours:
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
for b in buildings:
    if buildings_dict[b]["old_colours"] == False:
        pass
    else:
        f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
        f.write("\n// " + b + " switch to choose between old and modern colours")
        variants = list(buildings_dict[b]["variants"])
        for v in variants:
            heights = list(buildings_dict[b]["heights"])
            n = 0
            for h in heights:
                # Add the switch line and update details
                f = open("./src/houses/" + b + "/switches/colour_switches.pnml", "a")
                if v == 'x':
                    f.write("\n\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + h + "_sprites, current_year - age) {")
                else:
                    f.write("\n\nswitch (FEAT_HOUSES, SELF, switch_" + b + "_" + v + "_" + h + "_sprites, current_year - age) {")
                if v == 'x':
                    f.write("\n0.." + str(buildings_dict[b]["end_of_old_era"]) + ": switch_" + b + "_" + h + "_old;")  
                else:
                    f.write("\n0.." + str(buildings_dict[b]["end_of_old_era"]) + ": switch_" + b + "_" + v + "_" + h + "_old;")               
                if v == 'x':
                    f.write("\nswitch_" + b + "_" + h + "_modern;") 
                else:
                    f.write("\nswitch_" + b + "_" + v + "_" + h + "_modern;") 
                # Add bracket at the bottom
                f.write("\n}")
                f.close()
                n = n + 1