# import libraries
import cv2
import os
import re
import pytesseract as pyt
import numpy as np

# tesseract needs at least 300 dpi
# but our images lose accuracy when resizing
def resize_roi(img):

    idealw = 35
    idealh = 300
    cv2.imshow('original', img)
    if img.shape[0] < idealw or img.shape[1] < idealh:
        scale = idealh / img.shape[1]

        newx = int(img.shape[1] * scale)
        newy = int(img.shape[0] * scale)

        newimg = cv2.resize(img, (newx,newy))
        cv2.imshow('resized', newimg)

        return newimg
    else:
        return img

def sort_boxes(cnts):

    # sort by y first
    boxes = sorted(cnts, key=lambda y:y[1])
    # https://stackoverflow.com/questions/38805462/how-to-sort-contours-left-to-right-while-going-top-to-bottom-using-python-and
    # initially the line bottom is set to be the bottom of the first rect
    #boxes[][] = [[x, y, w+w, y+h]]
    line_bottom = boxes[0][3]

    line_begin_idx = 0

    for i in range(len(boxes)):
        # when a new box's top is below current line's bottom
        # it's a new line
        if boxes[i][1] > line_bottom:
            # sort the previous line by their x
            boxes[line_begin_idx:i] = sorted(boxes[line_begin_idx:i], key=lambda b: b[0])
            line_begin_idx = i
        # regardless if it's a new line or not
        # always update the line bottom
        line_bottom = max(boxes[i][3], line_bottom)
    # sort the last line
    boxes[line_begin_idx:] = sorted(boxes[line_begin_idx:], key=lambda b: b[0])

    return boxes

def detect_text(file):
    Image = cv2.imread(file)
    I = Image.copy()

    hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)

    G_Image = value

    padx = int(I.shape[0] * 0.15)
    pady = int(I.shape[1] * 0.15)

    # save path
    path = r"C:\Users\Oikawa\Desktop\ECE5470Project\bbroi"

    # make path if doesnt exist
    if not os.path.exists(path):
        os.makedirs(path)

    # delete contents of folder in path
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)

    # Otsu Thresholding
    # blur image
    blur = cv2.GaussianBlur(G_Image, (1, 1), 0)

    # get gradient
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(blur, cv2.MORPH_GRADIENT, kernel)

    # get threshold
    _, th = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # block of text
    # --- choosing the right kernel
    # --- kernel size of 3 rows (to join dots above letters 'i' and 'j')
    # --- and 10 columns to join neighboring letters in words and neighboring words
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 3))

    dilation = cv2.dilate(th, rect_kernel, iterations=1)

    # ---Finding contours of text block ---
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    wcnt = 0

    wordh = np.array([])
    wordw = np.array([])
    wordx = np.array([])
    wordy = np.array([])
    roi = []

    # rows = shape[0
    boxes = np.zeros((len(contours), 4))
    bcnt = 0


    for wordcontours in contours:
        (x, y, w, h) = cv2.boundingRect(wordcontours)

        boxes[bcnt][0] = x
        boxes[bcnt][1] = y
        boxes[bcnt][2] = x + w
        boxes[bcnt][3] = y + h

        bcnt = bcnt + 1

        wordh = np.append(wordh, h)
        wordw = np.append(wordw, w)
        wordx = np.append(wordx, x)
        wordy = np.append(wordy, y)

    # sort contours by y then x
    boxes = sort_boxes(boxes)
    avgh = sum(wordh) / len(wordh)
    avgw = sum(wordw) / len(wordw)

    for boxes1 in boxes:

        x, y, x2, y2 = boxes1
        x = int(x)
        y = int(y)
        x2 = int(x2)
        y2 = int(y2)
        w = x2 - x
        h = y2 - y

        wroi = []

        # detecting lines of text
        # height/width ratio should be under 0.5
        if (((I.shape[1] * 0.98) > h > avgh - (avgh * 0.45)) and (w > avgw - (avgw * 0.65))) and (0.01 < h/w < 0.5):

            wroi = I[y:y2, x:x2]

            # save word roi as img
            cv2.imwrite(path + "\word%d.jpg" % wcnt, wroi)

            wcnt = wcnt + 1
            roi.append([y, y2, x, x2])
            cv2.rectangle(I, (x, y), (x2, y2), (0, 255, 0), 1)

    # use later for character recognition
    text, sentence = tess_detect(path)

    return I, text, sentence

def tess_detect(imfilepath):

    pyt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    config = ("-l eng --oem 1 --psm 7")

    sen = ''

    for filename in os.listdir(imfilepath):
        if filename.endswith(".jpg"):

            img = cv2.imread(imfilepath + '\\' + filename)

            # get text from image
            text = pyt.image_to_string(img, config=config)

            # append text to list of all words
            sen = np.append(sen, text)

        # if another roi, add \n to indicate new line
        sen = np.append(sen, '\n')

    # join list to make string
    sentence = ''.join(sen)

    # copy sentence to text
    # this will be used to format output
    text = sentence

    # https://stackoverflow.com/questions/23996118/replace-special-characters-in-a-string-python
    # replace \n with ' ' for input to googletrans
    sentence = re.sub('[^a-zA-Z0-9\.]', ' ', sentence)

    return text, sentence
