import tkinter
import tkinter.ttk
from PIL import Image, ImageTk
import colorsys

class print_galaxy(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        
        master.title(u"galaxy")
        master.geometry("800x800")

        self.canvas = tkinter.Canvas(master, width = 800, height = 800)
        self.canvas.place(x=0, y=0)
        self.canvas.bind('<ButtonPress-1>', self.click)

        self.clickx = 0
        self.clicky = 0
        self.images = []  # to hold the newly created image

    def redraw(self, input_images=[[(1,1),(1,2),(1,3)],[(1,3),(1,4)]]):
        offset_x = 400
        offset_y = 400       
        for (image, i) in zip(input_images, range(len(input_images))):
            self.create_rectangle_with_alpha(0, 0, 800, 800, fill="black", outline="", alpha=0.4)
            for vec in image:
                col = self.hsv_to_colorcode(1.0 / len(input_images) * i, 1.0, 0.8)
                self.create_rectangle_with_alpha(offset_x+vec[0]*10, offset_y+vec[1]*10, offset_x+(vec[0]+1)*10, offset_y+(vec[1]+1)*10, fill=col, outline="", alpha=0.4)

    def click(self, event):
        self.images = []
        self.clickx = (event.x-400)//10
        self.clicky = (event.y-400)//10
        self.master.quit()
        print(self.clickx, self.clicky)
        return ((event.x-400)//10, (event.y-400)//10)

    def get_click_point(self):
        return (self.clickx, self.clicky)

    def create_rectangle_with_alpha(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def hsv_to_colorcode(self, h, s, v):
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        col = '#'
        if int(r*255) == 0:
            col += '00'
        else:
            col += format(int(r*255), 'x')
        if int(g*255) == 0:
            col += '00'
        else:
            col += format(int(g*255), 'x')
        if int(b*255) == 0:
            col += '00'
        else:
            col += format(int(b*255), 'x')
        return col

# state = nil
# vector = Vect(0, 0)
# root = tkinter.Tk()
# gui = print_galaxy(master=root)
# while(True):
#     # interact
#     # 前処理
#     gui.redraw(input_images)
#     gui.mainloop() # clickが動くまで無限ループ
#     vector = gui.get_click_point()
#     state = newState    