
from lib import buildingsjson

print("Running jpplusbuildings.py")

print("\tCreating Buildings JSON")
buildingsjson.CreateBuildingsJSON()

from lib import buildingsfiles

print("\tRunning CreateBuildingFiles")
buildingsfiles.CreateBuildingFiles()
