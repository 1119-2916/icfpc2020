import tkinter
import tkinter.ttk
from PIL import Image, ImageTk
import colorsys
from datetime import datetime

cell_size_list = [1, 2, 4, 6, 10, 20, 30, 50]

class print_galaxy(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.cell_size = 10
        self.cell_size_i = 5
 
        master.title(u"galaxy")
        master.geometry("1600x1000")

        self.width = 1600
        self.height = 1000
        self.offset_x = self.width/2
        self.offset_y = self.height/2

        self.canvas = tkinter.Canvas(master, width = self.width, height = self.height)
        self.canvas.place(x=0, y=0)
        self.canvas.bind('<ButtonPress-1>', self.click)
        self.canvas.bind('<ButtonPress-3>', self.save_state)
        self.canvas.bind("<Key>", self.key)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        now = datetime.now()
        self.filename = str(now.timestamp()) + ".txt"

        self.clickx = 0
        self.clicky = 0
        self.save_flag = 0
        self.images = []  # to hold the newly created image

    def setup_cell_i(self, layers):
        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0
        diffmax = 0

        for layer in layers:
            for vec in layer:
                xmin = min(vec[0], xmin)
                xmax = min(vec[0], xmax)
                ymin = min(vec[1], ymin)
                ymax = min(vec[1], ymax)

        diffmax = max(ymax - ymin, xmax - xmin)

        if diffmax <= 20:
            self.cell_size_i = 5
        elif diffmax <= 100:
            self.cell_size_i = 4
        elif diffmax <= 300:
            self.cell_size_i = 3
        else:
            self.cell_size_i = 2

    def setup_cell_size(self):
        if self.cell_size_i < 0:
            self.cell_size_i = 0
        elif self.cell_size_i >= len(cell_size_list):
            self.cell_size_i = len(cell_size_list) - 1
        self.cell_size = cell_size_list[self.cell_size_i]


    def save_state(self, event):
        print('save state!')
        self.save_flag = 1

    def redraw(self, input_images=[[(1,1),(1,2),(1,3)],[(1,3),(1,4)]]):
        self.last_image = input_images
        self.save_flag = 0

        self.setup_cell_size()

        self.create_rectangle_with_alpha(0, 0, self.width, self.height, fill="black", outline="", alpha=0.4)

        for (image, i) in zip(input_images, range(len(input_images))):
            for vec in image:
                col = self.hsv_to_colorcode(1.0 / len(input_images) * i, 1.0, 0.8)
                sx = int(self.offset_x+vec[0]*self.cell_size)
                sy = int(self.offset_y+vec[1]*self.cell_size)
                gx = int(self.offset_x+(vec[0]+1)*self.cell_size)
                gy = int(self.offset_y+(vec[1]+1)*self.cell_size)
                self.create_rectangle_with_alpha(sx, sy, gx, gy, fill=col, outline="", alpha=0.4)

    def log_click(self, event):
        self.images = []
        self.clickx = (int)(event.x-self.offset_x)//self.cell_size
        self.clicky = (int)(event.y-self.offset_y)//self.cell_size
        print("log {} {}".format(self.clickx, self.clicky))

    def key(self, event):
        print(event.char)

    def on_mouse_wheel(self, event):
        if event.delta < 0:
            self.zoom_out()
        elif event.delta > 0:
            self.zoom_in()

    def zoom_in(self):
        print("zoom_in...")
        self.cell_size_i += 1
        self.images = []
        self.master.quit()

    def zoom_out(self):
        print("zoom_out...")
        self.cell_size_i -= 1
        self.images = []
        self.master.quit()

    def click(self, event):
        self.images = []
        self.clickx = (int)(event.x-self.offset_x)//self.cell_size
        self.clicky = (int)(event.y-self.offset_y)//self.cell_size
        self.master.quit()
        print("click {} {}".format(self.clickx, self.clicky))

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

