import pandas as pd
import copy
from colourdict import colourdict as colourdict

# convert excel spreadsheet into dataframe
df1 = pd.read_excel('docs/buildings.xlsx','colours')

# convert dataframe into dictionary
raw_colour_profiles = df1.set_index('name').T.to_dict('dict')

colour_profile_names = list(raw_colour_profiles.keys())

for b in colour_profile_names:
    for c in colourdict:
        if pd.isna(raw_colour_profiles[b][c]) :
            pass
        else:
            raw_colour_profiles[b][c] = int(raw_colour_profiles[b][c])

colour_profiles = {}

colour_profiles = raw_colour_profiles.copy()
hirano = raw_colour_profiles["hirano_all_colours"].copy()

for b in colour_profile_names:
    colour_profiles[b] = {keys:values for keys, values in colour_profiles[b].items() if values is not None and values != 0}

print(colour_profiles)