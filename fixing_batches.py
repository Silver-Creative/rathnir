def fix_id(id: int):
    if id <= 767:
        return id #Land provinces remain unchanged
    elif id >= 7000 and id <= 7363:
        return id - 6232 #Sea provinces get moved back by 6232
    elif id >= 9000 and id <= 9040:
        return id - 7868 #Non-temporary wasteland provinces get moved back by 7868
    elif id >= 9500 and id <= 9618:
        return id - 8327 #Lake provinces get moved back by 8196
    elif id >= 9041 and id <= 9052:
        return id - 7749 #Temporary wasteland provinces get moved back by 7749
    elif id >= 9619 and id <= 9629:
        return id - 8315 #Temporary lake provinces get moved back by 8315
    else:
        return -1

with open('cleaner.txt', 'w') as f:
    for i in range(1, 9630):
        id_fixed = fix_id(i)
        if not id_fixed == -1:
            f.write(str(i) + ";" + str(fix_id(i)) + '\n')

with open('cleaner.txt', 'r') as f:
    sum = 0
    for line in f.readlines():
        sum = sum + int(line.split(";")[1])
    sum2 = 0
    for i in range(1, 1315):
        sum2 = sum2 + i
    
    if sum == sum2:
        print("yes")
    else:
        print("sum=" + str(sum) + ";sum2=" + str(sum2))
        print("no lmao")