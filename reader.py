import re
from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)
NumPat = re.compile(r'-?([1-9][0-9]*|0)')

def isNumerical(s):
    return NumPat.match(s)

def PARSE_FUNCTIONS(filename):
    res = {}

    with open(filename, 'r') as f:
        for line in f:
            if line == '':
                continue
            (name, expr) = PARSE_DEF(line)
            res[name] = expr

    return res


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



# ":1 = ap ap i 1"
# [":1", Ap(Atom('i'), Atom('1'))]
def PARSE_DEF(line):
    sp = line.split('=')
    name = sp[0].strip()
    expr_str = '='.join(sp[1:])
    parts = expr_str.strip().split()
    p = Parser(parts)
    expr = PARSE_ONE(p)
    return (name, expr)


def PARSE_ONE(p):
    head = p.get()[0]
    if head == 'ap':
        fun = PARSE_ONE(p)
        arg = PARSE_ONE(p)
        return Ap(fun, arg)

    return Atom(head)
