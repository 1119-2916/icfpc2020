#!/usr/bin/env python3

functions = None
state = nil
vector = Vect(0, 0)


class Expr:
    def __init__(self):
        self.Evaluated = None


class Atom(Expr):
    def __init__(self, Name):
        super().__init__()
        self.Name = Name


nil = Atom("nil")


class Ap(Expr):
    def __init__(self, Fun, Arg):
        super().__init__()
        self.Fun = Fun
        self.Arg = Arg


class Vect:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


def PARSE_FUNCTIONS(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        


def asNum(n): # Atom(Expr) -> number
    if (n is Atom)
        return PARSE_NUMBER(n.Name)
    ERROR("not a number")


def evalCons(a, b): # (Expr, Expr) -> Expr
    cons = Atom("cons")
    res = Ap(Ap(cons, eval(a)), eval(b))
    res.Evaluated = res
    return res


def eval(expr): # Expr -> Expr
    if (expr.Evaluated != None):
        return expr.Evaluated
    initialExpr = expr
    while (True):
        result = tryEval(expr)
        if (result == expr)
            initialExpr.Evaluated = result
            return result
        expr = result
 

def tryEval(expr): # Expr -> Expr
    t = Atom("t")
    f = Atom("f")

    if (expr.Evaluated != None):
        return expr.Evaluated
    if (expr is Atom && functions[expr.Name] != None):
        return functions[expr.Name]
    if (expr is Ap):
        fun = eval(expr.Fun)
        x = expr.Arg
        if (fun is Atom): # 1 arg
            if (fun.Name == "neg"):
                return Atom(-asNum(eval(x)))
            if (fun.Name == "i"):
                return x
            if (fun.Name == "nil"):
                return t
            if (fun.Name == "isnil"):
                return Ap(x, Ap(t, Ap(t, f)))
            if (fun.Name == "car"):
                return Ap(x, t)
            if (fun.Name == "cdr"):
                return Ap(x, f)
        if (fun is Ap):
            fun2 = eval(fun.Fun)
            y = fun.Arg
            if (fun2 is Atom): # 2 args
                if (fun2.Name == "t"):
                    return y
                if (fun2.Name == "f"):
                    return x
                if (fun2.Name == "add"):
                    return Atom(asNum(eval(x)) + asNum(eval(y)))
                if (fun2.Name == "mul"):
                    return Atom(asNum(eval(x)) * asNum(eval(y)))
                if (fun2.Name == "div"):
                    return Atom(asNum(eval(y)) / asNum(eval(x)))
                if (fun2.Name == "lt"):
                    return asNum(eval(y)) < asNum(eval(x)) ? t : f
                if (fun2.Name == "eq"):
                    return asNum(eval(x)) == asNum(eval(y)) ? t : f
                if (fun2.Name == "cons"):
                    return evalCons(y, x)
            if (fun2 is Ap):
                fun3 = eval(fun2.Fun)
                z = fun2.Arg
                if (fun3 is Atom): # 3 args
                    if (fun3.Name == "s"):
                        return Ap(Ap(z, x), Ap(y, x))
                    if (fun3.Name == "c"):
                        return Ap(Ap(z, x), y)
                    if (fun3.Name == "b"):
                        return Ap(z, Ap(y, x))
                    if (fun3.Name == "cons"):
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


if __name__ == '__main__':

    Map<string, Expr> functions = PARSE_FUNCTIONS("galaxy.txt")

    while(True):
        click = Ap(Ap(cons, Atom(vector.X)), Atom(vector.Y))
        (newState, images) = interact(state, click)
        PRINT_IMAGES(images)
        vector = REQUEST_CLICK_FROM_USER()
        state = newState
