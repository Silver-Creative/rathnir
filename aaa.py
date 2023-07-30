j = 1
statement = ""
for i in range(1323, 4977):
    statement = statement + str(i) + " "
    if j % 10 == 0:
        statement = statement + '\n'
    j = j + 1
print(statement)