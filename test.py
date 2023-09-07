from lib import functions

# This file creates the majority of building related pnml files, the exception being graphics ('gfx') pnml files
# It does not create centalised pnml files e.g. header.pnml  or src/functions files
# The purpose behind it was to be able to update building 'stats' and colour choices easily

print("Running jpplusbuildings.py")

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

