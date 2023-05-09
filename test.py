
import pandas
import json

Excel = pandas.read_excel('docs/buildings.xlsx', sheet_name='buildings')
Json = Excel.to_json(orient='records')

out_file = open("docs/buildings.json", "w")
json.dump(Json, out_file, indent = 6, separators=(", ", ": "))
out_file.close()