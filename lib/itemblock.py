
import json
from lib.functions import LoadJSON as LoadJSON

buildingsJSON = 'lib/buildings.json'
buildings = LoadJSON(buildingsJSON)

def ItemBlock(b):
    with open(r'./src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml', 'a') as file:
        # Parameter if needed
        if 'parameter'in buildings[b].keys():
            file.write("\n" + buildings[b]["parameter"])
        # Item Block Header
        file.write("\n// Item Block\n\titem(FEAT_HOUSES, item_" + b + ", " + str(buildings[b]["id"]) + ", " + str(buildings[b]["tile_size"])  + "){")
        # Properties Block
        file.write("\n\t\tproperty {")
        file.write("\n\t\t\tsubstitute:\t\t\t\t\t" +        str(buildings[b]["properties"]["substitute"]) + ";")
        if 'name' not in buildings[b]["graphics"].keys():
            file.write("\n\t\t\tname:\t\t\t\t\t\t" +        str(buildings[b]["properties"]["name"]) + ";")
        file.write("\n\t\t\tpopulation:\t\t\t\t\t" +        str(buildings[b]["properties"]["population"]) + ";")
        if 'building_flags' in list(buildings[b]["properties"].keys()):
            file.write("\n\t\t\tbuilding_flags:\t\t\t\t" +      str(buildings[b]["properties"]["building_flags"]) + ";")
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
        if 'name' in buildings[b]["graphics"].keys():
            file.write("\n\t\t\tname:\t\t\t\t\t\tswitch_" + b + "_name;")
        # Construction Check
        if 'construction_check' in buildings[b]["graphics"].keys():
            file.write("\n\t\t\tconstruction_check:\t\t\t"+ str(buildings[b]["graphics"]["construction_check"]) + ";")
        # Protection Check
        if 'protection' in buildings[b]["graphics"].keys():
            file.write("\n\t\t\tprotection:\t\t\t\t\t" +    str(buildings[b]["graphics"]["protection"]) + ";")
        file.write("\n\t\t\tcargo_production:\t\t\t" +      str(buildings[b]["graphics"]["cargo_production"]) + ";")
        # Foundations
        if 'foundations'in buildings[b]["graphics"].keys():
            file.write("\n\t\t\tfoundations:\t\t\t\t\t" +    str(buildings[b]["graphics"]["foundations"]) + ";")
        # Parameter
        if 'parameter'in buildings[b].keys():
            file.write("\n\t\t}\n\t}\n\t}\n")
        else: # Normal Item Block Closing
            file.write("\n\t\t}\n\t}\n")

        # Close file
        file.close()
