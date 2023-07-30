with open('cleaner.txt', 'r', encoding='ISO-8859-1') as cleaner:
    lines = cleaner.readlines()
data = ""
for line in lines:
    split = line.split(';')
    with open('map/area.txt', 'r', encoding='UTF-8') as areas:
        data = areas.read().replace(split[0], split[1])
        print(data)

with open('map/area2.txt', 'w', encoding='UTF-8') as areas2:
    areas2.write(data)