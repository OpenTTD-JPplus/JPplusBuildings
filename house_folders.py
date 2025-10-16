from lib.functions import LoadJSON as LoadJSON
import os

buildings_json = LoadJSON('lib/buildings.json')

json_folders = [buildings_json[b]['folder'] for b in buildings_json]

comp_folders = os.listdir('src/houses')

unused = [b for b in comp_folders if b not in json_folders]
print(f"Folders not used: {unused}")