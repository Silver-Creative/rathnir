import pandas as pd
import csv
import re
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

# [Config] we can't even add custom climate types so this isn't much of a "config" but yeah don't touch this please
climate_map = {
    "Tropical": "tropical",
    "Arid": "arid",
    "Arctic": "arctic",
    "Temperate": "temperate",
    "nan": "N/A",
    "-": "N/A"
}

winter_map = {
    "Winterless": "winterless",
    "Mild": "mild_winter",
    "Normal": "normal_winter",
    "Severe": "severe_winter",
    "nan": "N/A"
}

# Note: Does not yet support monsoons!

# [Logic] where the magic happens
with open('map/definition.csv', 'r', encoding='UTF-8') as definition:
    tropical = []
    arid = []
    arctic = []

    mild = []
    normal = []
    severe = []

    wip = []
    impassable = {}

    for line in definition.readlines():
        line_arr = line.split(";")
        if not line_arr[0].isnumeric():
            print(line)
            continue
        else:
            provID = int(line_arr[0])
            print("we are at " + str(provID))
            if provID > 4970:
                wip.append(provID)
            else:
                if df.at[provID-1, "type"] == "Wasteland":
                    continent = str(df.at[provID-1, "continent"])
                    try:
                        provlist = impassable[continent]
                    except:
                        impassable.update({continent: []})
                        provlist = impassable[continent]
                    
                    provlist.append(provID)

                if df.at[provID-1, "type"] == "Land":
                    climate_raw = df.at[provID-1, "climate"]
                    winter_raw = df.at[provID-1, "winters"]
                    climate = climate_map[climate_raw]
                    winter = winter_map[winter_raw]
                    match climate:
                        case "tropical":
                            tropical.append(provID)
                        case "arid":
                            arid.append(provID)
                        case "arctic":
                            arctic.append(provID)
                        case "temperate":
                            pass
                        case _:
                            print("Province " + str(provID) + " has no assigned climate!")
                    match winter:
                        case "mild_winter":
                            mild.append(provID)
                        case "normal_winter":
                            normal.append(provID)
                        case "severe_winter":
                            severe.append(provID)
                        case "winterless":
                            continue
                        case _:
                            print("Province " + str(provID) + " has no assigned winter!")

with open('map/climate.txt', 'w', encoding='UTF-8') as result:
    statement = ""

    # processing "tropical" provinces
    statement = statement + "\n#Example: Large parts of Africa and south east Asia\n"
    statement = statement + "tropical = {\n"
    tropical_as_string = ' '.join([str(provid) for provid in tropical])
    statement = statement + tropical_as_string + '\n'
    statement = statement + "}\n\n"

    # processing "arid" provinces
    statement = statement + "arid = {\n"
    arid_as_string = ' '.join([str(provid) for provid in arid])
    statement = statement + arid_as_string + '\n'
    statement = statement + "}\n\n"

    # processing "arctic" provinces
    statement = statement + "arctic = {\n"
    arctic_as_string = ' '.join([str(provid) for provid in arctic])
    statement = statement + arctic_as_string + '\n'
    statement = statement + "}\n\n"

    # processing "mild winter" provinces
    statement = statement + "\n#Example: Most of Europe north of med.\n"
    statement = statement + "mild_winter = {\n"
    mild_as_string = ' '.join([str(provid) for provid in mild])
    statement = statement + mild_as_string + '\n'
    statement = statement + "}\n\n"

    # processing "normal winter" provinces
    statement = statement + "\n#Example: Inland Europe & Scandinavian\n"
    statement = statement + "normal_winter = {\n"
    normal_as_string = ' '.join([str(provid) for provid in normal])
    statement = statement + normal_as_string + '\n'
    statement = statement + "}\n\n"

    # processing "severe winter" provinces
    statement = statement + "\n#Example: Russia & Lappland\n"
    statement = statement + "severe_winter = {\n"
    severe_as_string = ' '.join([str(provid) for provid in severe])
    statement = statement + severe_as_string + '\n'
    statement = statement + "}\n\n"

    # processing "impassable" provinces
    statement = statement + "impassable = {\n"
    for continent in impassable.keys():
        statement = statement + "\t#" + continent + '\n'
        provlist_as_string = ' '.join([str(provid) for provid in impassable[continent]])
        statement = statement + '\t' + provlist_as_string + '\n\n'
    
    statement = statement + "\t#Work in Progress\n"
    wip_as_string = ' '.join([str(provid) for provid in wip])
    statement = statement + '\t' + wip_as_string + '\n'
    statement = statement + "}\n\n"

    # TODO: processing monsoons
    statement = statement + "mild_monsoon = {\n\n}\n\nnormal_monsoon={\n\n}\n\nsevere_monsoon={\n\n}\n\n"
    statement = statement + "equator_y_on_province_image = 656\n"

    result.write(statement) 

    
