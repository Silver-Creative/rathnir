with open('localisation/replace/prov_names_l_english.yml', 'w', encoding='UTF-8-sig') as loca:
    with open('map/definition.csv', 'r', encoding='UTF-8') as definition:
        loca.write('l_english:\n')
        for line in definition.readlines():
            line_arr = line.split(";")
            if line_arr[0].isnumeric():
                loca.write(' PROV' + str(line_arr[0]) + ": \"" + line_arr[4] + '\"\n')