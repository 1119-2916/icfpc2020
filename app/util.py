from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)
from parse import (
    eval,
)

def check_nil(expr):
    expr = eval(expr)
    return (
        (type(expr) is Atom)
        and expr.Name == 'nil'
    )


def check_nonnull_list(expr):
    expr = eval(expr)
    if not (type(expr) is Ap):
        return False
    expr = eval(expr.Fun)
    if not (type(expr) is Ap):
        return False
    expr = eval(expr.Fun)
    if not (type(expr) is Atom):
        return False
    if not (expr.Name == 'cons'):
        return False
    return True

def check_list(expr):
    return (
        check_nil(expr)
        or check_nonnull_list(expr)
    )

def to_list(expr):
    res = []
    if not check_list(expr):
        raise Exception('invalid list!')
    while not check_nil(expr):
        head = eval(Ap(Atom('car'), expr))
        res.append(head)
        expr = eval(Ap(Atom('cdr'), expr))
        is_nil = eval(Ap(Atom('isnil'), expr))
        if type(expr) is Atom:
            if not check_nil(expr):
                res.append(expr)
            break
        if not check_list(expr):
            raise Exception('invalid list!')

    return res

def to_expr(vs):
    if type(vs) == list and len(vs) == 0:
        return nil
    if type(vs) == int:
        return Atom(str(vs))
    if isinstance(vs, Expr):
        return vs
    return Ap(Ap(Atom('cons'), to_expr(vs[0])), to_expr(vs[1:]))

def to_expr_vec(vs):
    if len(vs) < 2:
        raise Exception('vec should have at least two el')
    if len(vs) == 2:
        return Ap(Ap(Atom('cons'), Atom(str(vs[0]))), Atom(str(vs[1])))
    return Ap(Ap(Atom('cons'), Atom(str(vs[0]))), to_expr_vec(vs[1:]))


def mod_num(num):
    if num == 0:
        return '010'
    res = ''
    if num < 0:
        num = -num
        res += '10'
    else:
        res += '01'
    ln = 1
    pln = 4
    nowMax = 2 ** 4
    while nowMax <= num:
        ln += 1
        pln += 4
        nowMax *= 2 ** 4
    res += '1' * ln + '0'
    numstr = ''
    for i in range(pln):
        numstr += str(num % 2)
        num = num // 2
    return res + numstr[::-1]


def mod(expr):
    if type(expr) is Atom:
        if isNumerical(expr.Name):
            return mod_num(asNum(expr))
        if expr.Name == 'nil':
            return '00'
        raise Exception('parse error: mod: illegal num: {}'.format(expr.Name))
    return '11' + mod(eval(Ap(Atom('car'), expr))) + mod(eval(Ap(Atom('cdr'), expr)))

def dem_len_num(p):
    ln = 0
    while True:
        if p.isEnd():
            raise Exception('parse error: illegal number')
        if p.get() == '0':
            break
        ln += 4

    num = 0
    for i in range(ln):
        num *= 2
        num += int(p.get())

    return num


def dem0(p):
    head = p.get(2)
    if head == '00':
        return nil
    elif head == '01':
        return Atom(str(dem_len_num(p)))
    elif head == '10':
        return Atom(str(-1 * dem_len_num(p)))
    elif head == '11':
        e1 = dem0(p)
        e2 = dem0(p)
        return Ap(Ap(Atom('cons'), e1), e2)
    raise Exception('parse error: dem0')

def dem(bitseq):
    p = Parser(bitseq)
    return dem0(p)


class Parser:
    def __init__(self, ls):
        self.ls = ls
        self.ptr = 0

    def isEnd(self):
        return len(self.ls) <= self.ptr

    def peek(self, n=1):
        return self.ls[self.ptr : self.ptr+n]

    def get(self, n=1):
        s = self.ls[self.ptr : self.ptr+n]
        self.ptr += n
        return s


