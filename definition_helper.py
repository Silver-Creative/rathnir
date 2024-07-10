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

# [Config] to run this script, set this variable to the id of the last registered province (excluding the ones with ids in the 49xx-5000 range)
last_province = 4760       # touch this one
first_temp = 4977       # do not touch
max_provinces = 5000    # do not touch

# [Logic] the actual processing
with open('map/definition.csv', 'w', encoding='UTF-8', newline='') as def_file:
    writer = csv.writer(def_file)
    writer.writerow(["province", "red", "green", "blue", "x", "x"])
    i = 0
    for i in range(max_provinces - 1):
        if i+1 > last_province and i+1 < first_temp:
            continue
        id = str(df.at[i, 'id'])
        rgb = str(df.at[i, 'rgb'])
        x = str(df.at[i, 'name']).strip()
        row = [id, rgb, x, "x"]
        writer.writerow(row)

definition = open("map/definition.csv", encoding='UTF-8')
newtext = definition.read().replace(",", ";")
definition.close()

definition = open("map/definition.csv", "w", encoding='UTF-8')
definition.write(newtext)
definition.close()
