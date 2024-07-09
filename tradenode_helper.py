import pandas as pd
import csv

# [Options] may be useful for debugging
pd.options.display.max_rows = 9999
#pd.options.display.max_columns = 30
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)

# [Setup] leave as is, please
SHEET_ID = "1Hj_YOoVy9d6G0wkMezla6iDy7kvkiAXWyKNEhiECAWE"
SHEET_NAME = "Provinces"
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
df = df.drop(df.columns[30:41], axis = 1)
df.columns = ["name", "id", "type", "rgb", "area", "region", "superregion", "continent", "winters", "monsoons", "terrain", "climate", "is_colonized", "is_owned_by", "is_core_of", "is_city", "religion", "culture", "tradenode", "tradegood", "latentgood", "cot_rank", "base_tax", "base_production", "base_manpower", "total_development", "has_lv2_fort", "discovered_by", "prov_modifiers", "notes"]
df = df.dropna(axis=0, subset=['type'])

# [Config] please add all recognizable tradenodes to this!!
tradenode_map = {
    "Parmaletto": "parmaletto"
}

# tradenodes = ["Geshem Bay", "Theiotokos", "Caedan Sea", "Varmerien", "Ayesinco", "Eldal-Adadi", "Gebel", "Astyllean Sea", "Roscella", "Azethvir", "Arstedanna", "Sivan Sea", "Argentor", "Solea", "Lileanen", "Suderen", "Lotus Castle", "Serafini", "Voskovy", "Carvay", "Raykara", "Asturcia", "Knossos"]


# Note: Unlike most other scripts, simply running this script won't cut it.
#       This script will create a new file called "tradenode_helper_result.txt",
#       which contains the *mold* for the "members" section of the common/tradenodes file.
#       After running this script, you should copy the results onto the corresponding "members" section
#       of the tradenode you're editing.
#       Also, please delete the result textfile once you're done with it. Thanks!

# [Logic] where the magic happens
provnode_mapping = {}
for tradenode in tradenode_map.values():
    provnode_mapping.update({tradenode: [[],[]]}) # [[land tiles], [sea tiles]]

i = -1
last_province = 0
with open('map/definition.csv', 'r', encoding='UTF-8') as definition:
    for line in definition.readlines():
        i = i + 1
        line_arr = line.split(";")
        if not line_arr[0].isnumeric():
            print(line)
            continue
        else:
            provID = int(line_arr[0])
            if last_province == 0 and i != provID:
                last_province = i-1
            type_str = str(df.at[provID-1, 'type'])
            if not type_str in ["Open Sea Tile", "Coastal Sea Tile", "Inland Sea Tile", "Land"]:
                continue
            print("debug: we are in " + line_arr[4])
            tradenode_str = str(df.at[provID-1, 'tradenode'])
            tradenode = tradenode_map[tradenode_str]
            tradenode_tiles = provnode_mapping[tradenode]
            if type_str == "Land":
                tradenode_tiles[0].append(provID)
            else:
                tradenode_tiles[1].append(provID)


with open('tradenode_helper_result.txt', 'w', encoding='ISO-8859-1') as result:
    for tradenode in provnode_mapping:
        statement = tradenode + " = {\n"
        landtiles_list = provnode_mapping[tradenode][0]
        landtiles_string = ' '.join([str(tile) for tile in landtiles_list])
        seatiles_list = provnode_mapping[tradenode][1]
        seatiles_string = ' '.join([str(tile) for tile in seatiles_list])
        statement = statement + "\t#Land Tiles" + "\n\t" + landtiles_string + "\n\n"
        statement = statement + "\t#Sea Tiles" + "\n\t" + seatiles_string + "\n"
        statement = statement + "}" + "\n\n"
    result.write(statement)