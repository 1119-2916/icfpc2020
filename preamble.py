# 描画の前処理

from defs import (
    Expr,
    Atom,
    Ap,
    Vect,
    nil,
)
from parse import (
    eval,
    asNum,
)
from view import print_galaxy
import tkinter
import tkinter.ttk
from PIL import Image, ImageTk
import colorsys

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

def to_list(expr0):
    res = []
    expr = expr0
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

def to_expr_list(vs):
    if len(vs) == 0:
        return nil
    return Ap(Ap(Atom('cons'), Atom(str(vs[0]))), to_expr_vec(vs[1:]))

def to_expr_vec(vs):
    if len(vs) < 2:
        raise Exception('vec should have at least two el')
    if len(vs) == 2:
        return Ap(Ap(Atom('cons'), Atom(str(vs[0]))), Atom(str(vs[1])))
    return Ap(Ap(Atom('cons'), Atom(str(vs[0]))), to_expr_vec(vs[1:]))


def pre_vector(expr):
    return [asNum(expr2) for expr2 in to_list(expr)]

def pre_draw(expr):
    return [pre_vector(expr2) for expr2 in to_list(expr)]

def pre_multidraw(expr):
    return [pre_draw(expr2) for expr2 in to_list(expr)]

def proceed(proto, state, pt):
    res = eval(Ap(Ap(proto, state), pt))
    flag = asNum(eval(Ap(Atom('car'), res)))
    new_state = eval(Ap(Atom('car'), Ap(Atom('cdr'), res)))
    data = eval(Ap(Atom('car'), Ap(Atom('cdr'), Ap(Atom('cdr'), res))))

    if flag:
        return interact(proto, new_state, send_message(data))

    return (new_state, data)

def interact(proto=Atom('galaxy'), state=nil, pt=to_expr_vec([0, 0])):
    return proceed(proto, state, pt)


if __name__ == '__main__':
    # print(interact())
    stat = nil
    vector = [0, 0]
    root = tkinter.Tk()
    gui = print_galaxy(master=root)
    while(True):
        (newState, images) = interact(proto=Atom('galaxy'), state=stat, pt=to_expr_vec(vector))
        gui.redraw(pre_multidraw(images))
        gui.mainloop()
        pos = gui.get_click_point()
        vector = [pos[0], pos[1]]
        stat = newState
