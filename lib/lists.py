from lib import dictionaries, functions

# Create a list of buildings which will NOT be recoloured
def NoRecolouring():
    all_buildings = dictionaries.ItemsTab()
    buildings_no_recolouring = []
    for b in all_buildings:
        if all_buildings[b]["recolour"] == False:
            buildings_no_recolouring.append(all_buildings[b]["folder"])
        else:
            pass
    buildings_no_recolouring = list(dict.fromkeys(buildings_no_recolouring))
    return buildings_no_recolouring

# Create a list of buildings which will be recoloured
def Recolouring():
    all_buildings = dictionaries.ItemsTab()
    buildings_recolouring = []
    for b in all_buildings:
        if all_buildings[b]["recolour"] == False:
            pass
        else:
            buildings_recolouring.append(all_buildings[b]["folder"])
    buildings_recolouring = list(dict.fromkeys(buildings_recolouring))
    return buildings_recolouring

# Create a list of buildings which have old colours
def HasOldColours():
    all_buildings = dictionaries.ItemsTab()
    old_colour_buildings = []
    for b in all_buildings:
        if all_buildings[b]["old_colours"] == False:
            pass
        else: 
            old_colour_buildings.append(all_buildings[b]["folder"])
    old_colour_buildings = list(dict.fromkeys(old_colour_buildings))
    return old_colour_buildings