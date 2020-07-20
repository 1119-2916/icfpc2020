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
from api import (
    send_message,
)
from util import (
    to_list,
    to_expr_vec,
)

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
    layers = (pre_multidraw(interact()[1]))
    print(layers)
    layer_chars = ['#', '@']

    SZ = 15
    SZ2 = SZ * 2

    gamen = [['.' for j in range(SZ2)] for i in range(SZ2)]
    for i in range(len(layers)):
        layer = layers[i]
        for to in layer:
            print(to[0], to[1])
            gamen[SZ + to[0]][SZ + to[1]] = layer_chars[i]

    print('\n'.join([''.join(line) for line in gamen]))
