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
