from lib.dictionaries import ColoursAllWeightings as ColoursAllWeightings
from lib.dictionaries import ItemsTab as ItemsTab
from lib.functions import CreateRecolourPnml as CreateRecolourPnml
from lib.functions import CreateBuildingPalettes as CreateBuildingPalettes
from lib.functions import CreateRemapJSON as CreateRemapJSON
from lib.functions import CreateItemJSON as CreateItemJSON
from lib.functions import CreateItems as CreateItems
from lib.functions import CreateColourFiles as CreateColourFiles
from lib.functions import CreateColourSwitches as CreateColourSwitches
from lib.functions import CheckColourWeightingPresent as CheckColourWeightingPresent
from lib.functions import CheckBuildingSchema as CheckBuildingSchema
from lib.functions import CreateProbabilitiesJSON as CreateProbabilitiesJSON
from lib.functions import CreateNameSwitches as CreateNameSwitches
from lib.functions import NumHeights as NumHeights
from buildings import buildings_dict as buildings
import json

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

'''ColoursAllWeightings()

schema = LoadJSON('lib/buildings.json')

num_heights_dict = {x: schema[x]["heights"] for x in schema}
for b in num_heights_dict:
    heights = list(num_heights_dict[b].keys())
    for h in heights:
        num_heights_dict[b][h] = len(num_heights_dict[b][h])

#print(num_heights_dict)

print("New")
num_heights = {b: schema[b]["heights"] for b in schema}
print(num_heights)
print("aoki")
print(num_heights["aoki_office"])'''

#items = ItemsTab()
#print(ItemsTab())