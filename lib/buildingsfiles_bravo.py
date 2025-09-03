
import json
from lib.functions import LoadJSON as LoadJSON
from lib.itemblock import ItemBlock as ItemBlock
from lib.spritehandling import SpriteHandling as SpriteHandling

buildingsJSON = 'lib/buildings.json'
recolourJSON = 'lib/recolour.json'

recolour = LoadJSON(recolourJSON)
buildings = LoadJSON(buildingsJSON)

def CreateBuildingFilesBravo(b):

    # Open Logging
    with open(r'./lib/buildingfileslog.txt', 'a') as log:
        log.write('\n' + b)
        log.write('\n\tCODE STREAM: bravo')

        # Open Building file
        building_file = './src/houses/' + buildings[b]["folder"] + '/' + b + '.pnml'
        with open(building_file, 'w') as file:
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
            #non_standard_colour_basis = [b for b in buildings if buildings[b]["colours"]["basis"] != 'standard']
            
            if buildings[b]["colours"]["basis"] != 'standard':
                for l in levels:
                    updated_all_colours =  list(set(list(buildings[b]["colours"][l].keys())))
                    log.write('\n\t\tUpdated All Colours:\t' + l + ':\t' +str(updated_all_colours))
            else:
                updated_all_colours =  all_colours 

            # CREATE A FILE
            file.write("\n" + "// " + b + "\n")

        # SPRITEHANDLING
        log.write("\n\tSPRITE HANDLING")
        if 'childsprites' in list(buildings[b].keys()):
            childsprites = buildings[b]["childsprites"]
            log.write(f"\n\t\tChildsprites: \t\t{childsprites}")
            SpriteHandling(b,building_file, variants, levels, childsprites)
        else:
            log.write(f"\n\t\tNo Childsprites")
            SpriteHandling(b,building_file, variants, levels)
        
        # ITEM BLOCK
        log.write("\n\n\tITEM BLOCK")
        ItemBlock(b)

        # Close up shop
        log.close()
