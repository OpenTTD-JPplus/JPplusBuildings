
import json
from itertools import accumulate
from lib.functions import LoadJSON as LoadJSON
from lib.buildingsfiles_alpha import CreateBuildingFilesAlpha as CreateBuildingFilesAlpha
from lib.buildingsfiles_bravo import CreateBuildingFilesBravo as CreateBuildingFilesBravo
from lib.buildingsfiles_manual import CreateBuildingFilesManual as CreateBuildingFilesManual
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
        building_flaggers = [b for b in buildings if 'building_flags' in list(buildings[b]["properties"].keys())]

        # Close the log
        log.write('\n\nBUILDINGS')
        log.close()

        # Building by Building
        for b in buildings:
            if buildings[b]['code_stream'] == 'alpha':
                CreateBuildingFilesAlpha(b)
            elif buildings[b]['code_stream'] == 'bravo':
                CreateBuildingFilesBravo(b)
            elif buildings[b]['code_stream'] == 'manual':
                CreateBuildingFilesManual(b)
            elif buildings[b]['code_stream'] == 'charlie':
                pass
            else:
                print("YOLO!! " + b ) 
