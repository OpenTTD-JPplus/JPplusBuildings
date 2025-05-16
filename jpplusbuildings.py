
print("Running jpplusbuildings.py")

from lib import recolour

recolour.CreateRemapJSON()
recolour.CreateRecolourPnml()

from lib import buildingsjson

print("\tCreating Buildings JSON")
buildingsjson.CreateBuildingsJSON()

from lib import buildingsfiles

print("\tRunning CreateBuildingFiles")
buildingsfiles.CreateBuildingFiles()
