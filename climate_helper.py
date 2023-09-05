import pandas as pd
import csv
import re
import numpy as np

pd.options.display.max_rows = 9999

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)

SHEET_ID = "1Hj_YOoVy9d6G0wkMezla6iDy7kvkiAXWyKNEhiECAWE"
SHEET_NAME = "Provinces"
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
df = df.drop(df.columns[30:41], axis = 1)
df.columns = ["name", "id", "type", "rgb", "area", "region", "superregion", "continent", "winters", "monsoons", "terrain", "climate", "is_colonized", "is_owned_by", "is_core_of", "is_city", "religion", "culture", "tradenode", "tradegood", "latentgood", "cot_rank", "base_tax", "base_production", "base_manpower", "total_development", "has_lv2_fort", "discovered_by", "prov_modifiers", "notes"]
df = df.dropna(axis=0, subset=['type'])

climate_map = {
    "Tropical": "tropical",
    "Arid": "arid",
    "Arctic": "arctic",
    "Temperate": "temperate",
    "nan": "N/A",
    "-": "N/A"
}

with open('map/definition.csv', 'r', encoding='UTF-8') as definition:
    tropical = ""
    arid = ""
    arctic = ""
    for line in definition.readlines():
        line_arr = line.split(";")
        if not line_arr[0].isnumeric():
            print(line)
            continue
        else:
            provID = int(line_arr[0])
            if df.at[provID-1, "type"] == "Land":
                climate_raw = df.at[provID-1, "climate"]
                climate = climate_map[climate_raw]
                match climate:
                    case "tropical":
                        tropical = tropical + str(provID) + " "
                    case "arid":
                        arid = arid + str(provID) + " "
                    case "arctic":
                        arctic = arctic + str(provID) + " "
                    case "temperate":
                        continue
                    case _:
                        print("Province " + str(provID) + " has no assigned climate!")
    print("tropical = {")
    print('\t' + tropical)
    print("}")
    
    print("arid = {")
    print('\t' + arid)
    print("}")
    
    print("arctic = {")
    print('\t' + arctic)
    print("}")
    