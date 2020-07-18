import sys
import time

fmap = dict()

for raw in sys.stdin.readlines():
    line = raw.replace('\n', '')
    ops = line.split(' ')
    fmap[ops[0]] = ops[2:]

max_f_value = 0

for fname in fmap.keys():
    try:
        max_f_value = max(max_f_value, int(fname[1:]))
    except:
        continue

print(max_f_value)

bef = ""

def dfs(str):
    print("\ncall func" + str)
    global bef
    if bef == str:
        return
    bef = str
    time.sleep(0.1)
    solve = fmap[str]
    for i in solve:
        if i in fmap:
            dfs(i)
        else:
            print(i + ' ', end=' ')
    print()

#dfs('galaxy')
