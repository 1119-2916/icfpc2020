#!/usr/bin/env python3
import sys
sys.setrecursionlimit(4000)

from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)
from reader import (
    PARSE_FUNCTIONS,
    PARSE_EXPR,
)


def ERROR(s):
    raise Exception(s)

def PARSE_NUMBER(s):
    return int(s)

def cppdiv(a, b):
    return abs(a)//abs(b)*(1-((a>0)^(b>0))*2)


def asNum(n):  # Atom(Expr) -> number
    if type(n) is Atom:  # isinstance は継承元のクラスでも True を返す
        return PARSE_NUMBER(n.Name)
    ERROR("not a number")


def eval(expr_):
    EVAL = 0
    EVALCONS = 1
    TRYEVAL = 2

    STATE = 0
    EXPR = 1
    INITIALEXPR = 2
    A = 1
    B = 2
    FUN = 2
    X = 3
    FUN2 = 4
    Y = 5

    st = [[EVAL, [0, expr_, None]]]
    res = None
    while st:
        func, env = st[-1]
        if func == EVAL:
            expr = env[EXPR]
            if env[STATE] == 1:
                if res == expr:
                    env[INITIALEXPR].Evaluated = res
                    del st[-1]
                    continue
                env[EXPR] = res
                st.append([TRYEVAL, [0, res, None, None, None, None]])
            else:
                assert env[STATE] == 0
                if expr.Evaluated is not None:
                    res = expr.Evaluated
                    del st[-1]
                    continue
                env[INITIALEXPR] = expr
                st.append([TRYEVAL, [0, expr, None, None, None, None]])
                env[STATE] = 1
        elif func == EVALCONS:
            if env[STATE] == 0:
                st.append([EVAL, [0, env[A], None]])
                env[STATE] = 1
            elif env[STATE] == 1:
                env[A] = res
                st.append([EVAL, [0, env[B], None]])
                env[STATE] = 2
            else:
                assert env[STATE] == 2
                res = Ap(Ap(Atom("cons"), env[A]), res)
                res.Evaluated = res
                del st[-1]
        elif func == TRYEVAL:
            expr = env[EXPR]
            state = env[STATE]
            if state == 0:
                if expr.Evaluated is not None:
                    res = expr.Evaluated
                    del st[-1]
                elif type(expr) is Atom and functions.get(expr.Name) is not None:
                    res = functions.get(expr.Name)
                    del st[-1]
                elif type(expr) is Ap:
                    st.append([EVAL, [0, expr.Fun, None]])
                    env[STATE] = 1
                else:
                    res = expr
                    del st[-1]
            elif state == 1:
                env[FUN] = fun = res
                env[X] = x = expr.Arg
                if type(fun) is Atom:  # 1 arg
                    if fun.Name == "neg":
                        st.append([EVAL, [0, x, None]])
                        env[STATE] = 2
                        continue
                    elif fun.Name == "i":
                        res = x
                        del st[-1]
                        continue
                    elif fun.Name == "nil":
                        res = Atom("t")
                        del st[-1]
                        continue
                    elif fun.Name == "isnil":
                        res = Ap(x, Ap(Atom("t"), Ap(Atom("t"), Atom("f"))))
                        del st[-1]
                        continue
                    elif fun.Name == "car":
                        res = Ap(x, Atom("t"))
                        del st[-1]
                        continue
                    elif fun.Name == "cdr":
                        res = Ap(x, Atom("f"))
                        del st[-1]
                        continue
                if type(fun) is Ap:
                    st.append([EVAL, [0, fun.Fun, None]])
                    env[STATE] = 3
                    continue
                res = expr
                del st[-1]
            elif state == 2:
                res = Atom(-asNum(res))
                del st[-1]
            elif state == 3:
                env[FUN2] = fun2 = res
                env[Y] = y = env[FUN].Arg
                if type(fun2) is Atom:  # 2 args
                    if fun2.Name == "t":
                        res = y
                        del st[-1]
                        continue
                    elif fun2.Name == "f":
                        res = env[X]
                        del st[-1]
                        continue
                    elif fun2.Name in {"add", "mul", "div", "lt", "eq"}:
                        st.append([EVAL, [0, env[X], None]])
                        env[STATE] = 4
                        continue
                    elif fun2.Name == "cons":
                        st.append([EVALCONS, [0, y, env[X]]])
                        env[STATE] = 6
                        continue
                if type(fun2) is Ap:
                    st.append([EVAL, [0, fun2.Fun, None]])
                    env[STATE] = 7
                    continue
                res = expr
                del st[-1]
            elif state == 4:
                env[X] = res
                st.append([EVAL, [0, env[Y], None]])
                env[STATE] = 5
            elif state == 5:
                x = env[X]
                y = res
                fun2_Name = env[FUN2].Name
                if fun2_Name == "add":
                    res = Atom(asNum(x) + asNum(y))
                elif fun2_Name == "mul":
                    res = Atom(asNum(x) * asNum(y))
                elif fun2_Name == "div":
                    res = Atom(cppdiv(asNum(y), asNum(x)))
                elif fun2_Name == "lt":
                    res = Atom("t") if asNum(y) < asNum(x) else Atom("f")
                elif fun2_Name == "eq":
                    res = Atom("t") if asNum(x) == asNum(y) else Atom("f")
                else:
                    assert False
                del st[-1]
            elif state == 6:
                del st[-1]
            elif state == 7:
                fun3 = res
                x = env[X]
                y = env[Y]
                z = env[FUN2].Arg
                if type(fun3) is Atom:  # 3 args
                    if fun3.Name == "s":
                        res = Ap(Ap(z, x), Ap(y, x))
                    elif fun3.Name == "c":
                        res = Ap(Ap(z, x), y)
                    elif fun3.Name == "b":
                        res = Ap(z, Ap(y, x))
                    elif fun3.Name == "cons":
                        res = Ap(Ap(x, z), y)
                    else:
                        assert False, "b"
                        res = expr
                    del st[-1]
                    continue
                assert False, "a"
                res = expr
                del st[-1]
            else:
                assert False
        else:
            assert False
    return res




def evalCons(a, b):  # (Expr, Expr) -> Expr
    cons = Atom("cons")
    res = Ap(Ap(cons, eval(a)), eval(b))
    res.Evaluated = res
    return res

# def eval(expr):  # Expr -> Expr
#     if expr.Evaluated is not None:
#         return expr.Evaluated
#     initialExpr = expr
#     while True:
#         result = tryEval(expr)
#         if result == expr:
#             initialExpr.Evaluated = result
#             return result
#         expr = result

def tryEval(expr): # Expr -> Expr
    t = Atom("t")
    f = Atom("f")

    if expr.Evaluated is not None:
        return expr.Evaluated
    if type(expr) is Atom and functions.get(expr.Name) is not None:
        return functions.get(expr.Name)
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
                    assert False, "b"
                assert False, "a"
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


functions = {}
functions = PARSE_FUNCTIONS("galaxy.txt")

# print(functions)
# print({key: str(val) for (key, val) in functions.items()})

if __name__ == "__main__":
    #s = "galaxy"
    #s = "ap car ap cons 1 nil"
    #s = "ap ap ap s 0 1 ap ap ap s 2 3 ap ap ap s 4 5 6"
    s = 'ap car ap cdr ap cdr ap ap galaxy nil ap ap cons 0 0'
    e = eval(PARSE_EXPR(s))
    print(e)
