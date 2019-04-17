# import libraries
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
import text_detection as tdet

#https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Text Recognition")

        # layout
        self.HEIGHT = 700
        self.WIDTH = 700

        self.canvas = tk.Canvas(master, height=self.HEIGHT, width=self.WIDTH).pack()

        self.label = tk.Label(master, text="Select to choose a file. \tDetect text to process image.", bg='#B3CBF1', borderwidth = 5).place(relx = 0, rely = 0, relwidth = 1)

        self.label1 = tk.Label(master, text="Original Image", bg='#C0C0C0', borderwidth = 5).place(relx = 0.025, rely = 0.05, relwidth = 0.45)
        self.frame1 = tk.Canvas(master, bg='#808080', borderwidth=5).place(relx=0.025, rely=0.095, relwidth=0.45,relheight=0.4)

        self.label2 = tk.Label(master, text="Detected Text Regions", bg='#C0C0C0', borderwidth = 5).place(relx = 0.525, rely = 0.05, relwidth = 0.45)
        self.frame2 = tk.Canvas(master, bg='#808080', borderwidth=5).place(relx=0.525, rely=0.095, relwidth=0.45,relheight=0.4)

        self.label1 = tk.Label(master, text="Recognized Text", bg='#C0C0C0', borderwidth = 5).place(relx = 0.025, rely = 0.51, relwidth = 0.45)
        self.frame1 = tk.Canvas(master, bg='#808080', borderwidth=5).place(relx=0.025, rely=0.555, relwidth=0.45,relheight=0.4)

        self.label2 = tk.Label(master, text="Translated Text", bg='#C0C0C0', borderwidth = 5).place(relx = 0.525, rely = 0.51, relwidth = 0.45)
        self.frame2 = tk.Canvas(master, bg='#808080', borderwidth=5).place(relx=0.525, rely=0.555, relwidth=0.45,relheight=0.4)

        self.select_btn = tk.Button(master, text="Select", command=self.select_img)
        self.select_btn.pack(side = 'left', padx = 5, pady = 5)

        self.detect_btn = tk.Button(master, text="Detect Text", command=self.detect)
        self.detect_btn.pack(side = 'left', padx = 5, pady = 5)

        self.detect_btn = tk.Button(master, text="Translate Text", command=self.translate)
        self.detect_btn.pack(side = 'left', padx = 5, pady = 5)

        self.quit_btn = tk.Button(master, text="Quit", command=master.quit)
        self.quit_btn.pack(side='right', padx = 5, pady = 5)

    def select_img(self):
        self.file_path = filedialog.askopenfilename()

        try:
            img = cv2.imread(self.file_path)

            # https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter
            # Rearrange the color channel
            b, g, r = cv2.split(img)
            img = cv2.merge((r, g, b))

            # Convert the Image object into a TkPhoto object
            im = Image.fromarray(img)

            # Scale image for display
            h = im.size[1]
            w = im.size[0]

            imgscale = min((int(0.45 * self.WIDTH)/w), (int(0.4 * self.HEIGHT)/h))
            im = im.resize((int(imgscale * w), int(imgscale * h)), Image.ANTIALIAS)

            imgtk = ImageTk.PhotoImage(im)

            # Put it in the display window
            imgdis = tk.Canvas(self.master, bd=0, highlightthickness=0)
            imgdis.create_image(0, 0, image=imgtk, anchor= 'nw', tags="IMG")
            imgdis.place(relx=0.025, rely=0.1, relwidth=0.45,relheight=0.4)

            # save image as reference
            # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
            imgdis.image = imgtk

            return self.file_path

        except Exception as e:
            error = "Error"
            emessage = "Your file is either corrupted or not a valid image file.\nChoose another file.\n"

            messagebox.showerror(error, emessage + "Error: " + str(e))

    def detect(self):

        detected = tdet.detect_text(self.file_path)

        # https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter
        # Rearrange the color channel
        b, g, r = cv2.split(detected)
        dimg = cv2.merge((r, g, b))

        # Convert the Image object into a TkPhoto object
        dim = Image.fromarray(dimg)

        # Scale image for display
        h = dim.size[1]
        w = dim.size[0]

        imgscale = min((int(0.45 * self.WIDTH) / w), (int(0.4 * self.HEIGHT) / h))
        dim = dim.resize((int(imgscale * w), int(imgscale * h)), Image.ANTIALIAS)

        dimgtk = ImageTk.PhotoImage(dim)

        # Put it in the display window
        dimgdis = tk.Canvas(self.master, bd=0, highlightthickness=0)
        dimgdis.create_image(0, 0, image=dimgtk, anchor='nw', tags="IMG")
        dimgdis.place(relx=0.525, rely=0.1, relwidth=0.45, relheight=0.4)

        # save image as reference
        # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        dimgdis.image = dimgtk

    def print2window(self):
        print('test')

    def translate(self):
        print("test")

root = tk.Tk()
gui = GUI(root)
root.mainloop()