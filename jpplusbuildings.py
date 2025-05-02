
from lib import functions, buildingsjson, buildingsfiles

# This file creates the majority of building related pnml files, the exception being graphics ('gfx') pnml files
# It does not create centalised pnml files e.g. header.pnml  or src/functions files
# The purpose behind it was to be able to update building 'stats' and colour choices easily

print("Running jpplusbuildings.py")

print("\tCreating JSONs")
functions.CreateRemapJSON()
functions.CreateBuildingPalettes()
# New Function
buildingsjson.CreateBuildingsJSON()
# Old Function
functions.CreateItemJSON()
# Check if buildings in spreadsheet that shoyld have a recolour palette do
functions.CheckColourWeightingPresent()

print("\tRunning CreateBuildingFiles")
buildingsfiles.CreateBuildingFiles()

print("\tRunning CreateRecolourPnml")
functions.CreateRecolourPnml()

print("\tRunning CreateColourFiles")
functions.CreateColourFiles()

print("\tRunning CreateVariantFiles")
functions.CreateVariantFiles()

print("\tRunning CreateLevelsFiles")
functions.CreateLevelsFiles()

print("\tRunning CreateColourSwitches")
functions.CreateColourSwitches()

print("\tRunning CreateDirectionSwitches")
functions.CreateDirectionSwitches()

print("\tRunning CreateNameSwitches")
functions.CreateNameSwitches()

print("\tRunning PnmlCombiner")
functions.PnmlCombiner()

print("\tRunning CreateItems")
functions.CreateItems()