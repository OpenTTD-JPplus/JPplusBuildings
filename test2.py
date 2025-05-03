
import json
from lib.buildingsfiles import GetPointsLevels as GetPointsLevels

buildingsJSON = 'lib/new_buildings.json'
recolourJSON = 'lib/recolour.json'

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

recolour = LoadJSON(recolourJSON)
buildings = LoadJSON(buildingsJSON)

points = GetPointsLevels("shiro","all")
print(points)



