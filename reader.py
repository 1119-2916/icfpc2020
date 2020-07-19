from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)

def PARSE_FUNCTIONS(filename):
    res = {}

    with open(filename, 'r') as f:
        line = f.readline()
        print(line)
        (name, expr) = PARSE_DEF(line)
        res[name] = expr

    res


# ":1 = ap ap i 1"
# [":1", Ap(Atom('i'), Atom('1'))]
def PARSE_DEF(line):
    sp = line.split('=')
    name = sp[0].strip()
    expr_str = '='.join(sp[1:])
    parts = expr_str.strip().split()
    print(name, parts)
    return (name, expr)
