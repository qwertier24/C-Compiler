import sys
sys.stdin = open("c.txt", "r")
sys.stdout = open("changed_c.txt", "w")

V = set()
for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    line = line.split('->')
    l = line[0].strip()
    r = line[1].split(' ')
    V.add(l)

sys.stdin = open("c.txt", "r")
for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    line = line.split('->')
    l = line[0].strip()
    r = line[1].split(' ')
    print("[", l, ']', end=' --> ', sep='')
    for s in r:
        if s != '':
            if s in V:
                print('[', s, ']', end=' ', sep='')
            else:
                print('"', s, '"', end=' ', sep='')
    print()
