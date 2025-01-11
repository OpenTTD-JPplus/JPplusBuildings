from lib import dictionaries, functions

# Create a list of buildings which will NOT be recoloured
def ActiveBuildings():
    all_buildings = dictionaries.ItemsTab()
    active_buildings = []

    for b in all_buildings:
        if all_buildings[b]["include"] != False:
            active_buildings.append(all_buildings[b]["folder"])
    active_buildings = list(dict.fromkeys(active_buildings))
    return active_buildings

def ActiveBuildingItems():
    all_buildings = dictionaries.ItemsTab()
    active_building_items = []

    for b in all_buildings:
        if all_buildings[b]["include"] != False:
            active_building_items.append(b)
    return active_building_items

def ParameterBuildings():
    all_buildings = dictionaries.ItemsTab()
    parameter_buildings = []

    for b in all_buildings:
        if all_buildings[b]["param_top"] != "none":
            parameter_buildings.append(b)
    return parameter_buildings

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

# Create a list of buildings which have name switches
def HasNameSwitch():
    all_buildings = dictionaries.ItemsTab()
    name_switch_buildings = []
    for b in all_buildings:
        if all_buildings[b]["name_switch"] == "none":
            pass
        else:
            name_switch_buildings.append(all_buildings[b]["folder"])
            name_switch_buildings = list(dict.fromkeys(name_switch_buildings))
    return name_switch_buildings