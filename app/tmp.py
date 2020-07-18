import sys
import resource

print(sys.getrecursionlimit())
sys.setrecursionlimit(3000)

seica = {}
class iter:
    def __init__(self, s, pla = 0):
        self.lis = s.split()
        self.pla = pla

    def inc(self):
        self.pla += 1
    
    def get(self):
        return self.lis[self.pla]

def read(s):
    this_top = s.get()
    this_id = s.pla
    print('in read {} {}: in'.format(this_top, this_id))
    if s.get() != 'ap':
        if s.get().isdecimal():
            return [int(s.get())]
        elif s.get() in seica:
            return seica[s.get()]
        else:
            print('error in read: ' + s.get() + ' is invalid')
            return False

    left = None
    right = None
    
    s.inc()
    print('in read {} {}: left is {}'.format(this_top, this_id, s.get()))
    if s.get() == 'ap':
        left = read(s)
    elif s.get() in seica:
        left = seica[s.get()]
    else:
        print('error in read left: ' + s.get() + ' is invalid')

    s.inc()
    print('in read {} {}: right is {}'.format(this_top, this_id, s.get()))
    if s.get() == 'ap':
        right = read(s)
    elif s.get().isdecimal():
        right = [int(s.get())]
    elif s.get() in seica:
        right = seica[s.get()]
    else:
        print('error in read right: ' + s.get() + ' is invalid')
    
 
    print('in read {} {}: end {} {}'.format(this_top, this_id, left, right))
    try:
        return left.excute(right)
    except Exception as e:
        return False


class abst:
    def excute(self, x):
        pass

class cons1(abst):
    def __init__(self, x):
        self.value = x

    def excute(self, x):
        print('cons1 excute: {} {}'.format(self.value, x))
        ret = []
        if type(self.value) == type([]):
            ret = [*self.value]
        else:
            ret = [self.value]
        if type(x) == type([]):
            ret = [*ret, *x]
        else:
            ret = [*ret, x]

        print('after excute: {}'.format(ret))
        return ret

class con(abst):
    def excute(x):
        return cons1(x)

class add1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return [self.value[0] + x[0]]

class add(abst):
    def excute(x):
        return add1(x)

class inc(abst):
    def excute(x):
        return [x[0] + 1]

class dec(abst):
    def excute(x):
        return [x[0] - 1]

class mul1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return [self.value[0] * x[0]]

class mul(abst):
    def excute(x):
        return mul1(x)

class div1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return [self.value[0] / x[0]]

class div(abst):
    def excute(x):
        return div1(x)

class t1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return self.value

class t(abst):
    def excute(x):
        return t1(x)

class f1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return x

class f(abst):
    def excute(x):
        return f1(x)

class eq1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        if self.value[0] == x[0]:
            return t
        else:
            return f

class eq(abst):
    def excute(x):
        return eq1(x)

class lt1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        if self.value[0] < x[0]:
            return t
        else:
            return f

class lt(abst):
    def excute(x):
        return lt1(x)

class mod(abst):
    def excute(x):
        return [bin(x[0])]

class dem(abst):
    def excute(x):
        return [int(x[0])]

class neg(abst):
    def excute(x):
        return [-x[0]]

class c2(abst):
    def __init__(self, x1, x2):
        self.value1 = x1
        self.value2 = x2
    
    def excute(self, x):
        print('c2 excute: {} {} {}'.format(self.value1, self.value2, x))
        tmp = self.value1.excute(x)
        return tmp.excute(self.value2)

class c1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return c2(self.value, x)

class c(abst):
    def excute(x):
        return c1(x)

class b2(abst):
    def __init__(self, x1, x2):
        self.value1 = x1
        self.value2 = x2
    
    def excute(self, x):
        print('b2 excute: {} {} {}'.format(self.value1, self.value2, x))
        tmp = self.value2.excute(x)
        return self.value1.excute(tmp)

class b1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return b2(self.value, x)

class b(abst):
    def excute(x):
        return b1(x)

class s2(abst):
    def __init__(self, x1, x2):
        self.value1 = x1
        self.value2 = x2
    
    def excute(self, x):
        left = self.value1.excute(x)
        right = self.value2.excute(x)
        return left.excute(right)

class s1(abst):
    def __init__(self, x):
        self.value = x
    
    def excute(self, x):
        return s2(self.value, x)

class s(abst):
    def excute(x):
        return s1(x)

class i(abst):
    def excute(x):
        return x

class isnil(abst):
    def excute(x):
        if x == []:
            return t
        else:
            return f

class car(abst):
    def excute(x):
        return [x[0]]

class cdr(abst):
    def excute(x):
        return [x[-1]]

seica['nil'] = []
seica['cons'] = con
seica['add'] = add
seica['inc'] = inc
seica['dec'] = dec
seica['mul'] = mul
seica['div'] = div
seica['t'] = t
seica['f'] = f
seica['eq'] = eq
seica['lt'] = lt
seica['mod'] = mod
seica['dem'] = dem
seica['neg'] = neg
seica['c'] = c
seica['b'] = b
seica['s'] = s
seica['i'] = i
seica['isnil'] = isnil
seica['car'] = car
seica['cdr'] = cdr


now = iter('ap ap cons 8398848 ap ap cons 8407040 ap ap cons 8398849 ap ap cons 8407041 ap ap cons 8398850 ap ap cons 8402946 ap ap cons 8407042 ap ap cons 8398851 ap ap cons 8402947 ap ap cons 8407043 ap ap cons 8398852 ap ap cons 8402948 ap ap cons 8407044 ap ap cons 8390661 ap ap cons 8394757 ap ap cons 8398853 ap ap cons 8402949 ap ap cons 8407045 ap ap cons 8411141 ap ap cons 8415237 ap ap cons 8402950 nil')
print(read(now))
print(read(iter('ap ap ap c add 2 1')))
print(read(iter('ap ap ap b inc dec 1')))
print(read(iter('ap ap ap s mul ap add 1 6')))
print(read(iter('ap isnil ap ap cons 1 nil')))
print(read(iter('ap isnil nil')))


readed_cou = 0
with open('galaxy.txt', 'r') as file:
    lines = []
    readed = {}
    while True:
        line = file.readline()
        if not line:
            break
        lines.append(line)
        
    while True:
        flag = True
        for line in lines:
            lis = line.split()
            print('now is {}'.format(lis[0]))
            if lis[0] in readed:
                continue
        
            res = read(iter(line, 2))
            '''
            try:
                res = read(iter(line, 2))
            except Exception as e:
                print(e)
                continue
            '''
            
            if res == False:
                continue
            if type(res) == type([]) and None in res:
                continue

            seica[lis[0]] = res
            readed[lis[0]] = True
            flag = False
            readed_cou += 1
            print(lis[0], res)
        
        if flag:
            break
'''
    for line in lines:
        lis = line.split()
        print('now is {}'.format(lis[0]))
        if lis[0] in seica:
            continue

        seica[lis[0]] = seica['nil']
        
    while True:
        flag = True
        for line in lines:
            lis = line.split()
            print('now is {}'.format(lis[0]))
            if lis[0] in readed:
                continue
        
            # res = read(iter(line, 2))
            try:
                res = read(iter(line, 2))
            except Exception as e:
                print(e)
                continue
            
            if res == False:
                continue

            seica[lis[0]] = res
            readed[lis[0]] = True
            flag = False
            readed_cou += 1
            print(lis[0], res)
        
        if flag:
            break
'''
for key, value in seica.items():
    print(key, value)

print(len(seica))