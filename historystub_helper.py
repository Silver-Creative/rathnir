import pandas as pd
import csv
import re
import numpy as np
import os

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

tech_groups = ["tech_alteniquian", "tech_vastallosi", "tech_niedene", "tech_luthic", "tech_vraelean", "tech_aldoviri"]
religion_map = {
    "Hukar Sharud": "hukar_sharud",
    "Theiosism": "theiosism",
    "Sakrelism": "sakrelism",
    "Red Cult": "red_cult",
    "Soleannen": "soleannen",
    "Dandelism": "dandelism",
    "Aegmerism": "aegmerism",
    "Etherflame": "etherflame",
    "Zentivar": "zentivar",
    "Cardinalism": "cardinalism",
    "Sanderosa": "sanderosa",
    "Asharu": "asharu",
    "Eastern Asharu": "eastern_asharu",
    "SparNative": "norse",
    "Tossanism": "tossanism",
    "Abyss Mysticism": "abyss_mysticism",
    "Willowpact": "willowpact",
    "Noxism": "noxism",
    "Asitir": "asitir",
    "Twin Dragon": "twin_dragon",
    "Vinaestre": "vinaestre",
    "Lotus Doctrine": "lotus_doctrine"
}

def f_remove_accents(old):
    """
    Removes common accent characters, lower form.
    Uses: regex.
    """
    new = old.lower()
    new = re.sub(r'[àáâãäå]', 'a', new)
    new = re.sub(r'[èéêë]', 'e', new)
    new = re.sub(r'[ìíîï]', 'i', new)
    new = re.sub(r'[òóôõö]', 'o', new)
    new = re.sub(r'[ùúûü]', 'u', new)
    return new

with open('map/definition.csv', 'r', encoding='UTF-8') as definition:
    for line in definition.readlines():
        line_arr = line.split(";")
        if not line_arr[0].isnumeric():
            print(line)
            continue
        else:
            provID = int(line_arr[0])
            provNAME = str(line_arr[4])
            filename = str(provID) + " - " + provNAME.replace("?", "").replace("/", "-")
            
            histpath = str(os.getcwd()) + '\history\provinces'
            for file in os.listdir(histpath):
                if file.startswith(str(provID)):
                    os.remove(histpath + '\\' + file)

            if not df.at[provID-1, 'type'] == "Land":
                with open('history/provinces/' + filename + ".txt", "w+", encoding='ISO-8859-1') as history:
                    history.write("# " + filename + '\n')
                    history.write('\n')
                    if provID < 4000:
                        for tech_group in tech_groups:
                            history.write("discovered_by = " + tech_group + "\n")
            else:
                owner = str(df.at[provID-1, 'is_owned_by'])
                if str(df.at[provID-1, 'is_core_of']) == "nan":
                    core_of = [owner]
                else:
                    core_of = str(df.at[provID-1, 'is_core_of']).split(";")
                culture = f_remove_accents(str(df.at[provID-1, 'culture'])).lower().replace(" ", "_")
                religion = religion_map[str(df.at[provID-1, 'religion'])]

                base_tax = df.at[provID-1, 'base_tax']
                if np.isnan(base_tax):
                    base_tax = 1
                else:
                    base_tax = int(base_tax)
                
                base_production = df.at[provID-1, 'base_production']
                if np.isnan(base_production):
                    base_production = 1
                else:
                    base_production = int(base_production)
                
                base_manpower = df.at[provID-1, 'base_manpower']
                if np.isnan(base_manpower):
                    base_manpower = 1
                else:
                    base_manpower = int(base_manpower)

                goods = str(df.at[provID-1, 'tradegood']).lower().strip().replace(" ", "_")
                cot = int(df.at[provID-1, 'cot_rank'])

                is_city = str(df.at[provID-1, 'is_colonized']).lower()

                fort = str(df.at[provID-1, 'has_lv2_fort']).lower()

                with open('history/provinces/' + filename + ".txt", "w+", encoding='ISO-8859-1') as history:
                    history.write("# " + filename + '\n')
                    history.write('\n')
                    if is_city == "yes":
                        history.write("owner = " + owner + '\n')
                        history.write("controller = " + owner + '\n')
                        for cored in core_of:
                            history.write("add_core = " + cored + '\n')
                        history.write('\n')
                    history.write("culture = " + culture + '\n')
                    history.write("religion = " + religion + '\n')
                    history.write("capital = \"\"\n")
                    history.write('\n')
                    history.write("hre = no\n")
                    history.write('\n')
                    history.write("base_tax = " + str(base_tax) + '\n')
                    history.write("base_production = " + str(base_production) + '\n')
                    history.write("base_manpower = " + str(base_manpower) + '\n')
                    history.write('\n')
                    history.write("trade_goods = " + goods + '\n')
                    if not cot == 0:
                        history.write("center_of_trade = " + str(cot) + '\n')
                    history.write('\n')
                    history.write("is_city = " + is_city + '\n')
                    history.write("fort_15th = " + fort + '\n')
                    history.write('\n')
                    for tech_group in tech_groups:
                        history.write("discovered_by = " + tech_group + "\n")
