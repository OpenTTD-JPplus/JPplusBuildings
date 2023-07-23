import pandas as pd

# convert into dataframe
df1 = pd.read_excel("docs/buildings.xlsx")

# convert into dictionary
dict = df1.to_dict()

name = list(dict["name"].values())
include = list(dict["include"].values())
folder = list(dict["folder"].values())

items_dictionary = {name[i]:include[i] for i in range(len(name))}
buildings_dictionary = {folder[i]:include[i] for i in range(len(name))}

all_building_items = list(items_dictionary.keys())
all_buildings = list(buildings_dictionary.keys())

building_items = []
for b in all_building_items:
    if items_dictionary[b] == True:
        building_items.append(b)
    else:
        pass

buildings = []
for b in all_buildings:
    if buildings_dictionary[b] == True:
        buildings.append(b)
    else:
        pass

print(buildings)



