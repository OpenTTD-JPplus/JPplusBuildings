import pandas as pd

# convert into dataframe
df1 = pd.read_excel("docs/buildings.xlsx")

# convert into dictionary
dict = df1.to_dict()

name = (dict["name"].values())
id = (dict["id"].values())
tile_size = (dict["tile_size"].values())

id_dict = dict(name,id,tile_size)

print(id_dict["fukuda"])


id_slots = list(range(0,256))


