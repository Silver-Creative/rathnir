import string

import pandas as pd
import csv
import numpy as np

# [Options] may be useful for debugging
pd.options.display.max_rows = 9999
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

# [Config] please add all recognizable continents to this!!
continent_map = {
    "Alteniquia": "alteniquia",
    "Nieden": "nieden",
    "Syltor": "syltor",
    "Sparwood": "sparwood",
    "Haven": "haven",
    "The North": "the_north",
    "Valdreach": "valdreach",
    "Plagos": "plagos",
    "Akan'nash": "akannash"
}

# [Logic] where the magic happens
provlist_mapping = {}
for continent in continent_map.values():
    provlist_mapping.update({continent: []})

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
            if not df.at[provID-1, 'type'] == "Land":
                continue
            print("debug: we are in " + line_arr[4])
            continent_str = str(df.at[provID-1, 'continent'])
            continent = continent_map[continent_str]
            prov_list = provlist_mapping[continent]
            prov_list.append(provID)

with open('map/continent.txt', 'w', encoding='ISO-8859-1') as result:
    for continent in provlist_mapping:
        statement = continent + " = {\n"
        prov_list = provlist_mapping[continent]
        provs_string = ' '.join([str(prov) for prov in prov_list])
        statement = statement + "\t" + provs_string + "\n"
        statement = statement + "}" + "\n\n"

    base_game_section = "### Base Game\neurope = {\n\n}\n\nasia = {\n\n}\n\nafrica = {\n\n}\n\nnorth_america = {\n\n}\n\nsouth_america = {\n\n}\n\noceania = {\n\n}\n\n"
    
    debug_continent_section = "debug_continent = { #unused province ids go here to prevent errors. if an id is present in 2 continents, it will create an error, so they're easy to find\n"
    debug_string = ' '.join([str(id) for id in range(last_province+1, 5000)])
    debug_continent_section = debug_continent_section + '\t' + debug_string + '\n'
    debug_continent_section = debug_continent_section + "}\n\n"

    last_section = "island_check_provinces = {\n\n}\n\n# Used for RNW\nnew_world = {\n\n}\n"

    statement = statement + base_game_section + debug_continent_section + last_section
    result.write(statement)