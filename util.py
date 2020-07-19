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


