import pandas as pd
import csv

pd.options.display.max_rows = 9999
#pd.options.display.max_columns = 30

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

tradenodes = ["Geshem Bay", "Theiotokos", "Caedan Sea", "Varmerien", "Ayesinco", "Eldal-Adadi", "Gebel", "Astyllean Sea", "Roscella", "Azethvir", "Arstedanna", "Sivan Sea", "Argentor", "Solea", "Lileanen", "Suderen", "Lotus Castle", "Serafini", "Voskovy", "Carvay", "Raykara", "Asturcia", "Knossos"]
for tradenode in tradenodes:
    statement = ""
    print(tradenode + "= {\n")
    for i in range(768):
        if df.loc[i, 'tradenode'] == tradenode:
            statement = statement + str(i + 1) + " "
    print('\t' + statement)
    print("}\n")