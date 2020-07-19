#!/usr/bin/env python3
import sys
sys.setrecursionlimit(100000)

from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)
from reader import PARSE_FUNCTIONS


def ERROR(s):
    raise Exception(s)

def PARSE_NUMBER(s):
    return int(s)

def cppdiv(a, b):
    return abs(a)//abs(b)*(1-((a>0)^(b>0))*2)


def asNum(n): # Atom(Expr) -> number
    if type(n) is Atom:  # isinstance は継承元のクラスでも True を返す
        return PARSE_NUMBER(n.Name)
    ERROR("not a number")

def evalCons(a, b): # (Expr, Expr) -> Expr
    cons = Atom("cons")
    res = Ap(Ap(cons, eval(a)), eval(b))
    res.Evaluated = res
    return res

def eval(expr): # Expr -> Expr
    if expr.Evaluated is not None:
        return expr.Evaluated
    initialExpr = expr
    while True:
        result = tryEval(expr)
        if result == expr:
            initialExpr.Evaluated = result
            return result
        expr = result

def tryEval(expr): # Expr -> Expr
    t = Atom("t")
    f = Atom("f")

    if expr.Evaluated is not None:
        return expr.Evaluated
    if type(expr) is Atom and functions[expr.Name] is not None:
        return functions[expr.Name]
    if type(expr) is Ap:
        fun = eval(expr.Fun)
        x = expr.Arg
        if type(fun) is Atom: # 1 arg
            if fun.Name == "neg":
                return Atom(-asNum(eval(x)))
            if fun.Name == "i":
                return x
            if fun.Name == "nil":
                return t
            if fun.Name == "isnil":
                return Ap(x, Ap(t, Ap(t, f)))
            if fun.Name == "car":
                return Ap(x, t)
            if fun.Name == "cdr":
                return Ap(x, f)
        if type(fun) is Ap:
            fun2 = eval(fun.Fun)
            y = fun.Arg
            if type(fun2) is Atom: # 2 args
                if fun2.Name == "t":
                    return y
                if fun2.Name == "f":
                    return x
                if fun2.Name == "add":
                    return Atom(asNum(eval(x)) + asNum(eval(y)))
                if fun2.Name == "mul":
                    return Atom(asNum(eval(x)) * asNum(eval(y)))
                if fun2.Name == "div":
                    return Atom(cppdiv(asNum(eval(y)), asNum(eval(x))))
                if fun2.Name == "lt":
                    return t if asNum(eval(y)) < asNum(eval(x)) else f
                if fun2.Name == "eq":
                    return t if asNum(eval(x)) == asNum(eval(y)) else f
                if fun2.Name == "cons":
                    return evalCons(y, x)
            if type(fun2) is Ap:
                fun3 = eval(fun2.Fun)
                z = fun2.Arg
                if type(fun3) is Atom: # 3 args
                    if fun3.Name == "s":
                        return Ap(Ap(z, x), Ap(y, x))
                    if fun3.Name == "c":
                        return Ap(Ap(z, x), y)
                    if fun3.Name == "b":
                        return Ap(z, Ap(y, x))
                    if fun3.Name == "cons":
                        return Ap(Ap(x, z), y)
    return expr


def interact(state, event): # (flag, newstate, data) -> (newstate, multipledraw)
    expr = Ap(Ap(Atom("galaxy"), state), event)
    res = eval(expr)
    # Note: res will be modulatable here (consists of cons, nil and numbers only)
    [flag, newState, data] = GET_LIST_ITEMS_FROM_EXPR(res)
    if (asNum(flag) == 0):
        return (newState, data)
    return interact(newState, SEND_TO_ALIEN_PROXY(data))

def main():
    state = nil
    vector = Vect(0, 0)
    while(True):
        click = Ap(Ap(cons, Atom(vector.X)), Atom(vector.Y))
        (newState, images) = interact(state, click)
        PRINT_IMAGES(images)
        vector = REQUEST_CLICK_FROM_USER()
        state = newState


# これを動くようにしてほしい
# functions = {}
# print(eval(Ap(Atom('i'), Atom('1'))))



functions = PARSE_FUNCTIONS("galaxy.txt")
print(functions)
print({key: str(val) for (key, val) in functions.items()})
