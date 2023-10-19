import pandas as pd
import csv
import numpy as np

pd.options.display.max_rows = 9999
#pd.options.display.max_columns = 30

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)

SHEET_ID = "1SlTa-Gms9BLTrIdChqVDow0WE3W8MVfi9u51JXNuyQA"
SHEET_NAME = "Provinces"
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
df = df.drop(df.columns[30:41], axis = 1)
df.columns = ["name", "id", "type", "rgb", "area", "region", "superregion", "continent", "winters", "monsoons", "terrain", "climate", "is_colonized", "is_owned_by", "is_core_of", "is_city", "religion", "culture", "tradenode", "tradegood", "latentgood", "cot_rank", "base_tax", "base_production", "base_manpower", "total_development", "has_lv2_fort", "discovered_by", "prov_modifiers", "notes"]
df = df.dropna(axis=0, subset=['type'])

#print(df)
with open('map/definition.csv', 'w', encoding='UTF-8', newline='') as def_file:
    writer = csv.writer(def_file)
    writer.writerow(["province", "red", "green", "blue", "x", "x"])
    i = 0
    for i in range(4999):
        if i+1 > 2052 and i+1 < 4977:
            continue
        #if str(df.loc[i, 'id']) != "4999":
        id = str(df.at[i, 'id'])
        rgb = str(df.at[i, 'rgb'])
        x = str(df.at[i, 'name']).strip()
        row = [id, rgb, x, "x"]
        #print(row)
        writer.writerow(row)
        #else:
        #    break

#terraintypes = ["Glacial", "Farmlands", "Forest", "Hills", "Woods", "Mountains", "Grasslands", "Jungle", "Marsh", "Desert", "Coastal Desert", "Coastline", "Drylands", "Highlands", "Savannah", "Steppe"]
#for terrain in terraintypes:
#    statement = ""
#    j = 1
#    print(terrain + "= {\n")
#    for i in range(767):
#        #print("debug: i=" + str(i) + ";loc=" + df.loc[i, 'terrain'] + ";terrain=" + terrain + ";yes?=" + str(df.loc[i, 'terrain'] == terrain))
#        if df.loc[i, 'terrain'] == terrain:
#            statement = statement + str(i+1) + " "
#            if j % 20 == 0:
#                statement = statement + '\n'
#        j = j + 1
#    print('\t' + statement)
#    print("}\n")

#seatypes = ["Inland Sea Tile", "Coastal Sea Tile", "Open Sea Tile"]
#for seatype in seatypes:
#    statement = ""
#    print(seatype + "= {\n")
#    for i in range(767, 1132):
#        if df.loc[i, 'type'] == seatype:
#            statement = statement + str(i + 1) + " "
#    print('\t' + statement)
#    print("}\n")

#print(df)
