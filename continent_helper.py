import string

def get_provinces_from_area(area: str):
    with open('map/area.txt', 'r') as areas:
        lines = areas.readlines()
        for i in range(0, len(lines)):
            if lines[i].startswith(area):
                return lines[i+1].split()

def get_areas_from_region(region: str):
    areas = []
    in_place = False
    with open('map/region.txt', 'r') as regions:
        lines = regions.readlines()
        for i in range(0, len(lines)):
            if in_place and lines[i].startswith("areas"):
                continue
            if in_place:
                j = 0
                while True:
                    ix = i + j
                    if lines[ix].startswith("}"):
                        return areas[1:-1]
                    elif not lines[ix].isspace() and not lines[ix].startswith("areas"):
                        areas.append(lines[ix][:-6].strip())
                    j = j + 1
            if lines[i].startswith(region):
                in_place = True
                continue
            
def get_regions_from_superregion(superregion: str):
    in_place = False
    regions = []
    with open('map/superregion.txt', 'r') as superregions:
        lines = superregions.readlines()
        for i in range(0, len(lines)):
            if in_place:
                j = 0
                while True:
                    ix = i + j
                    if lines[ix].startswith("}"):
                        return regions[1:]
                    elif not lines[ix].startswith("\trestrict_charter"):
                        regions.append(lines[ix][1:-8])
                    j = j+1
            if lines[i].startswith(superregion):
                in_place = True
                continue

def prepare_statement_for_continent(continent_name: str, continent: list):
    statement = continent_name + " = {\n"
    regions = []
    for superregion in continent:
        regions = get_regions_from_superregion(superregion)
        for region in regions:
            print(region)
            statement = statement + "\t# " + string.capwords(region.replace("_", " ")) + "\n"
            provs_total = []
            areas = get_areas_from_region(region)
            for area in areas:
                provs_total = provs_total + get_provinces_from_area(area)
            provs_string = ' '.join([str(prov) for prov in provs_total])
            statement = statement + "\t" + provs_string + "\n"
    statement = statement + "}" + "\n"
    return statement


alteniquia = ["essukdal", "aldovir", "vastallos"]
nieden = ["varmerien", "asterien"]
sparwood = ["western_sparwood"]
print(prepare_statement_for_continent("nieden", nieden))