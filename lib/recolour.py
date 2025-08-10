
import json
import pandas as pd

def ExportToJSON(dictionary, target_file):
    with open(target_file, 'w') as fp:
        json.dump(dictionary, fp, indent=4)
        fp.close()

def LoadJSON(target_file):
    with open(target_file, 'r') as file:
        data = json.load(file)
    return data

def non_nan_value(item):
    k, v = item
    return v != 'nan'

recolour_codes  = {
        'palette01': '0xC6: 0x', 
        'palette02': '0xC7: 0x', 
        'palette03': '0xC8: 0x', 
        'palette04': '0xC9: 0x', 
        'palette05': '0xCA: 0x', 
        'palette06': '0xCB: 0x', 
        'palette07': '0xCC: 0x', 
        'palette08': '0xCD: 0x',
        'palette09': '0x50: 0x', 
        'palette10': '0x51: 0x', 
        'palette11': '0x52: 0x', 
        'palette12': '0x53: 0x', 
        'palette13': '0x54: 0x', 
        'palette14': '0x55: 0x', 
        'palette15': '0x56: 0x', 
        'palette16': '0x57: 0x',
        'palette17': '0x88: 0x',
        'palette18': '0x89: 0x',
        'palette19': '0x8A: 0x',
        'palette20': '0x8B: 0x',
        'palette21': '0x8C: 0x',
        'palette22': '0x8D: 0x',
        'palette23': '0x8E: 0x',
        'palette24': '0x8F: 0x',
        }

palette_numbers = list(recolour_codes.keys())

def CreateRemapJSON():
    # convert excel spreadsheet into dataframe
    df1 = pd.read_excel('docs/buildings.ods','colours')
    df2 = df1.drop('option', axis=1)
    df3 = df2[df2['name'].str.contains('remap|palette', case=False)]
    df4 = df3.set_index('name').transpose()

    all_columns = list(df4) # Creates list of all column headers
    palette_columns = [x for x in all_columns if "palette" in x]
    
    for p in palette_columns:
        df4[p] = df4[p].astype(str).str.zfill(2)

    # convert dataframe into dictionary
    raw_colour_profiles = df4.T.to_dict('dict')

    colour_profiles = {}
    for k, v in raw_colour_profiles.items():
        if isinstance(v, dict):
            colour_profiles[k] = dict(filter(non_nan_value, v.items()))
        else:
            colour_profiles[k] = v

    ExportToJSON(colour_profiles, 'lib/recolour.json')

def CreateRecolourPnml():
    recolour_json = LoadJSON('lib/recolour.json')

    # Create Recolour.pnml file
    website1 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Recolour_sprites'
    website2 = '// https://newgrf-specs.tt-wiki.net/wiki/NML:Builtin_functions'

    
    with open('src/recolour.pnml', 'w') as f:
        f.write(website1)
        f.write('\n\n' + website2 + '\n\n')
        f.write('recolour_remap = reserve_sprites(' + str(len(recolour_json)) + ');\n\n')
        f.write('replace(recolour_remap) {\n')
        f.close()
    for c in recolour_json:
        replacements = list(recolour_json[c].keys())
        replacements.remove('remap')
        with open('src/recolour.pnml', 'a') as f:
            f.write('\n// ' + c + " +" + str(recolour_json[c]["remap"]))
            f.write('\n\trecolour_sprite {')
            for r in replacements:
                f.write('\n\t\t' + recolour_codes[r] + str(recolour_json[c][r]) + ';')
            f.write("\n\t}")
            f.close()
    with open('src/recolour.pnml', 'a') as f:
        f.write("\n}")
        f.close()
