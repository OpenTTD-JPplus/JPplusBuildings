
from lib import functions

# This file creates the majority buildings related pnml files, exception being graphics ('gfx') pnml files
# It does not create centalised pnml files e.g. header.pnml  or src/functions files
# The purpose behind it was to be able to update building 'stats' and colour choinse easily

print("Running jpplusbuildings.py")

print("\tRunning ImportColoursTab")
functions.ImportColoursTab()

print("\tRunning CreateColourFiles")
functions.CreateColourFiles()

print("\tRunning CreateVariantFiles")
functions.CreateVariantFiles()

print("\tRunning CreateLevelsFiles")
functions.CreateLevelsFiles()

print("\tRunning CreateColourSwitches")
functions.CreateColourSwitches()