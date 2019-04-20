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

        self.mainframe = tk.Frame(master, bg = '#FFFFFF')
        self.mainframe.pack()

        self.canvas = tk.Canvas(self.mainframe, width = self.WIDTH, height = self.HEIGHT, bg = '#FFFFFF')
        self.canvas.pack()

        #
        self.frame1 = tk.Frame(self.canvas, bg = '#B3CBF1')
        self.frame1.grid(row = 1, columnspan = 2, ipadx = 30, ipady = 5, pady = 15)

        self.label1 = tk.Label(self.frame1, text = "\t***\tSelect an image file.\t*** \tDetect text to process.\t***\t", bg='#B3CBF1')
        self.label1.pack(fill = 'x', side = 'left', padx = 100, anchor = 'center', expand = True)

        #
        self.frame2 = tk.Frame(self.canvas, bg = '#FFFFFF')
        self.frame2.grid(row = 2, columnspan = 2, pady = 2)

        self.label2 = tk.Label(self.frame2, text = "Original Image", bg='#FFFFFF')
        self.label2.pack(side = 'left', ipadx = 150, padx = 38, fill = 'x', expand = True, anchor = 'center')

        self.label3 = tk.Label(self.frame2, text = "Detected Regions", bg='#FFFFFF')
        self.label3.pack(side = 'right', ipadx = 146, padx = 39, fill = 'x', expand = True, anchor = 'center')

        #
        self.canvas1 = tk.Canvas(self.canvas, bg='#808080')
        self.canvas1.grid(row = 3, column = 0, pady = 5)

        self.canvas2 = tk.Canvas(self.canvas, bg='#808080')
        self.canvas2.grid(row = 3, column = 1, pady = 5)

        #
        self.frame3 = tk.Frame(self.canvas, bg = '#FFFFFF')
        self.frame3.grid(row = 4, columnspan = 2, pady = 5)

        self.label4 = tk.Label(self.frame3, text = "Detected Text", bg='#FFFFFF')
        self.label4.pack(side = 'left', ipadx = 150, padx = 38, fill = 'x', expand = True, anchor = 'center')

        self.label5 = tk.Label(self.frame3, text = "Translated Text", bg='#FFFFFF')
        self.label5.pack(side = 'right', ipadx = 146, padx = 39, fill = 'x', expand = True, anchor = 'center')

        #
        self.canvas3 = tk.Canvas(self.canvas, bg='#808080')
        self.canvas3.grid(row = 5, column = 0, pady = 5)

        self.canvas4 = tk.Canvas(self.canvas, bg='#808080')
        self.canvas4.grid(row = 5, column = 1, pady = 5)

        #
        self.select_btn = tk.Button(self.frame1, text="Select", command=self.select_img)
        self.select_btn.pack(side = 'right', ipadx = 40, padx = 40)

        #
        self.detect_btn = tk.Button(self.mainframe, text="Detect Light Text", command=self.detect)
        self.detect_btn.pack(side = 'left', ipadx = 10, padx = 10, pady = 10)

        self.detect_btn_inv = tk.Button(self.mainframe, text="Detect Dark Text", command=self.detect2)
        self.detect_btn_inv.pack(side = 'left', ipadx = 10, padx = 10, pady = 10)

        self.translate_btn = tk.Button(self.mainframe, text="Translate Text", command=self.print_translated_text)
        self.translate_btn.pack(side = 'left', anchor = 'center', ipadx = 10, padx = 10, pady = 10)

        self.quit_btn = tk.Button(self.mainframe, text="Quit", command=master.quit)
        self.quit_btn.pack(side = 'right', anchor = 'center', padx = 10, pady = 10)

    def testdef(self):
        print('works')

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

            # size of the canvas
            cw = self.canvas3.winfo_width()
            ch = self.canvas3.winfo_height()

            imgscale = min((int(cw)/w), (int(ch)/h))
            im = im.resize((int(imgscale * w), int(imgscale * h)), Image.ANTIALIAS)

            imgtk = ImageTk.PhotoImage(im)

            # Put it in the display window
            self.canvas1.create_image((cw-1)/2, (ch-1)/2, image=imgtk, anchor= 'center', tags="IMG")

            # save image as reference
            # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
            self.canvas1.image = imgtk

            return self.file_path

        except Exception as e:
            error = "Error"
            emessage = "Your file is either corrupted or not a valid image file.\nChoose another file.\n"

            messagebox.showerror(error, emessage + "Error: " + str(e))

    def img2canvas(self, detected):
        # https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter
        # Rearrange the color channel
        b, g, r = cv2.split(detected)
        dimg = cv2.merge((r, g, b))

        # Convert the Image object into a TkPhoto object
        dim = Image.fromarray(dimg)

        # Scale image for display
        h = dim.size[1]
        w = dim.size[0]

        # size of the canvas
        cw = self.canvas3.winfo_width()
        ch = self.canvas3.winfo_height()

        imgscale = min((int(cw) / w), (int(ch) / h))
        dim = dim.resize((int(imgscale * w), int(imgscale * h)), Image.ANTIALIAS)

        dimgtk = ImageTk.PhotoImage(dim)

        # Put it in the display window
        self.canvas2.create_image((cw - 1) / 2, (ch - 1) / 2, image=dimgtk, anchor='center', tags="IMG")

        # save image as reference
        # http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        self.canvas2.image = dimgtk

    def detect(self):
        detected = tdet.detect_text(self.file_path)
        self.img2canvas(detected)

    def detectinv(self):
        detected = tdet.detect_text_inv(self.file_path)
        self.img2canvas(detected)

    def detect2(self):
        detected = tdet.detect_text2(self.file_path)
        self.img2canvas(detected)

    def print_detected_text(self):
        # clear old text
        self.canvas3.delete('all')

        # size of the canvas
        w = self.canvas3.winfo_width()
        h = self.canvas3.winfo_height()

        text = "Hello World\nCanvas 3"

        # find the length of the string
        # for placement
        x = w - len(text)

        xplace = (x-1)/2
        yplace = (h-1)/2

        self.canvas3.create_text(xplace, yplace, text = text, fill="black", font="Times 10", width = w - 50, anchor = 'center')

    def print_translated_text(self):
        # clear old text
        self.canvas4.delete('all')

        # size of the canvas
        w = self.canvas4.winfo_width()
        h = self.canvas4.winfo_height()

        # placeholder for testing
        text = "ora"

        # find the length of the string
        # for placement
        x = w - len(text)

        xplace = (x-1)/2
        yplace = (h-1)/2

        self.canvas4.create_text(xplace, yplace, text = text, fill="black", font="Times 10", width = w - 50, anchor = 'center')

root = tk.Tk()
gui = GUI(root)
root.mainloop()