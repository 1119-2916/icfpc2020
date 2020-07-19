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
    st = [["eval", {"expr": expr_, "state": 0}]]
    res = None
    while st:
        func, env = st[-1]
        if func == "eval":
            if env["state"] == 1:
                env["result"] = res
                if env["result"] == env["expr"]:
                    env["initialExpr"].Evaluated = env["result"]
                    res = env["result"]
                    del st[-1]
                    continue
                env["expr"] = env["result"]
                st.append(["tryEval", {"expr": env["expr"], "state": 0}])
            elif env["state"] == 0:
                if env["expr"].Evaluated is not None:
                    res = env["expr"].Evaluated
                    del st[-1]
                    continue
                env["initialExpr"] = env["expr"]
                st.append(["tryEval", {"expr": env["expr"], "state": 0}])
                env["state"] = 1
            else:
                assert False
        elif func == "evalCons":
            if env["state"] == 0:
                st.append(["eval", {"expr": env["a"], "state": 0}])
                env["state"] = 1
            elif env["state"] == 1:
                env["a"] = res
                st.append(["eval", {"expr": env["b"], "state": 0}])
                env["state"] = 2
            elif env["state"] == 2:
                env["b"] = res
                res = Ap(Ap(Atom("cons"), env["a"]), env["b"])
                res.Evaluated = res
                del st[-1]
            else:
                assert False
        elif func == "tryEval":
            if env["state"] == 0:
                env["t"] = Atom("t")
                env["f"] = Atom("f")
                if env["expr"].Evaluated is not None:
                    res = env["expr"].Evaluated
                    del st[-1]
                    continue
                if type(env["expr"]) is Atom and functions.get(env["expr"].Name) is not None:
                    res = functions.get(env["expr"].Name)
                    del st[-1]
                    continue
                if type(env["expr"]) is Ap:
                    st.append(["eval", {"expr": env["expr"].Fun, "state": 0}])
                    env["state"] = 1
                    continue
                res = env["expr"]
                del st[-1]
            elif env["state"] == 1:
                env["fun"] = res
                env["x"] = env["expr"].Arg
                if type(env["fun"]) is Atom:  # 1 arg
                    if env["fun"].Name == "neg":
                        st.append(["eval", {"expr": env["x"], "state": 0}])
                        env["state"] = 2
                        continue
                    if env["fun"].Name == "i":
                        res = env["x"]
                        del st[-1]
                        continue
                    if env["fun"].Name == "nil":
                        res = env["t"]
                        del st[-1]
                        continue
                    if env["fun"].Name == "isnil":
                        res = Ap(env["x"], Ap(env["t"], Ap(env["t"], env["f"])))
                        del st[-1]
                        continue
                    if env["fun"].Name == "car":
                        res = Ap(env["x"], env["t"])
                        del st[-1]
                        continue
                    if env["fun"].Name == "cdr":
                        res = Ap(env["x"], env["f"])
                        del st[-1]
                        continue
                if type(env["fun"]) is Ap:
                    st.append(["eval", {"expr": env["fun"].Fun, "state": 0}])
                    env["state"] = 3
                    continue
                res = env["expr"]
                del st[-1]
            elif env["state"] == 2:
                res = Atom(-asNum(res))
                del st[-1]
            elif env["state"] == 3:
                env["fun2"] = res
                env["y"] = env["fun"].Arg
                if type(env["fun2"]) is Atom:  # 2 args
                    if env["fun2"].Name == "t":
                        res = env["y"]
                        del st[-1]
                        continue
                    if env["fun2"].Name == "f":
                        res = env["x"]
                        del st[-1]
                        continue
                    if env["fun2"].Name in {"add", "mul", "div", "lt", "eq"}:
                        st.append(["eval", {"expr": env["x"], "state": 0}])
                        env["state"] = 4
                        continue
                    if env["fun2"].Name == "cons":
                        st.append(["evalCons", {"a": env["y"], "b": env["x"], "state": 0}])
                        env["state"] = 6
                        continue
                if type(env["fun2"]) is Ap:
                    st.append(["eval", {"expr": env["fun2"].Fun, "state": 0}])
                    env["state"] = 7
                    continue
                res = env["expr"]
                del st[-1]
            elif env["state"] == 4:
                env["x"] = res
                st.append(["eval", {"expr": env["y"], "state": 0}])
                env["state"] = 5
            elif env["state"] == 5:
                env["y"] = res
                if env["fun2"].Name == "add":
                    res = Atom(asNum(env["x"]) + asNum(env["y"]))
                elif env["fun2"].Name == "mul":
                    res = Atom(asNum(env["x"]) * asNum(env["y"]))
                elif env["fun2"].Name == "div":
                    res = Atom(cppdiv(asNum(env["y"]), asNum(env["x"])))
                elif env["fun2"].Name == "lt":
                    res = env["t"] if asNum(env["y"]) < asNum(env["x"]) else env["f"]
                elif env["fun2"].Name == "eq":
                    res = env["t"] if asNum(env["x"]) == asNum(env["y"]) else env["f"]
                else:
                    assert False
                del st[-1]
            elif env["state"] == 6:
                del st[-1]
            elif env["state"] == 7:
                env["fun3"] = res
                env["z"] = env["fun2"].Arg
                if type(env["fun3"]) is Atom:  # 3 args
                    if env["fun3"].Name == "s":
                        res = Ap(Ap(env["z"], env["x"]), Ap(env["y"], env["x"]))
                    elif env["fun3"].Name == "c":
                        res = Ap(Ap(env["z"], env["x"]), env["y"])
                    elif env["fun3"].Name == "b":
                        res = Ap(env["z"], Ap(env["y"], env["x"]))
                    elif env["fun3"].Name == "cons":
                        res = Ap(Ap(env["x"], env["z"]), env["y"])
                    else:
                        assert False, "b"
                        res = env["expr"]
                    del st[-1]
                    continue
                assert False, "a"
                res = env["expr"]
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
