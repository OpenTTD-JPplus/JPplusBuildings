import pandas as pd

with open("test_manual.pnml") as manual:
    manual_lines = [line.rstrip('\n') for line in manual]

with open("test_generated.pnml") as generated:
    generated_lines = [line.rstrip('\n') for line in generated]

differing_v1 = []
for element in manual_lines:
    if element not in generated_lines:
        differing_v1.append(element)

print(differing_v1)

differing_v2 = []
for element in generated_lines:
    if element not in manual_lines:
        differing_v2.append(element)

print(differing_v2)


'''# convert excel spreadsheet into dataframe
df1 = pd.read_excel("docs/buildings.xlsx")

# convert dataframe into dictionary
all_buildings = df1.set_index('name').T.to_dict('dict')

# create active, inactive and parameter building lists

folders = list(df1["folder"])
folders = list(dict.fromkeys(folders))

f = open("./src/houses.pnml", "w")
f.write('\n// House pnml files\n')
f.close()
for b in folders:
    f = open("./src/houses.pnml", "a")
    f.write('\n#include "src/houses/' + b + '/' + b + '.pnml"')
    f.close()'''