invalid_lines = []

f = open("spend_big2.csv", 'r')

line_num = 2

line = f.readline()
line = f.readline()

while line:
    items = [x for x in line.strip('\n').split(',') if x != '']
    # print(len(items), items, '\n')
    
    if len(items) != 10 or items[3] == '0':
        invalid_lines.append(line_num)
    
    line_num += 1
    
    line = f.readline()

f.close()

print(len(invalid_lines))
print(line_num)