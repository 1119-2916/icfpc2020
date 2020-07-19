# 描画の前処理
import sys

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
from preamble import (
    interact,
    pre_multidraw,
)
from util import (
    to_expr_vec,
)
from view import print_galaxy
import tkinter
import tkinter.ttk
from PIL import Image, ImageTk
import colorsys
from datetime import datetime

sys.setrecursionlimit(1000000)

stat = nil
vector = [-1000, 0]
root = tkinter.Tk()
gui = print_galaxy(master=root)
next_upd = True
while(True):
    if next_upd:
        (newState, images) = interact(proto=Atom('galaxy'), state=stat, pt=to_expr_vec(vector))

    next_upd = False
    gui.redraw(pre_multidraw(images))
    print('done')
    gui.mainloop()

    if gui.clickx is not None:
        print('calculating...')
        pos = gui.get_click_point()
        if gui.save_flag == 1:
            print(stat)
        now = datetime.now()
        filename = str(now.timestamp()) + ".txt"
        print("write log: {}".format("logs/" + filename))
        with open("logs/" + filename, mode='a') as f:
            f.write(str(stat)+"\n")
        vector = [pos[0], pos[1]]
        stat = newState
        next_upd = True

    gui.clickx = None
