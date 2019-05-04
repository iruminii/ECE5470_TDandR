# import libraries
import cv2
import os
import numpy as np
import holefiller as hf
from tkinter import messagebox
import predict as p


# import the necessary packages
import numpy as np


#  Felzenszwalb et al.
def non_max_suppression_slow(boxes, overlapThresh = 0.3):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list, add the index
        # value to the list of picked indexes, then initialize
        # the suppression list (i.e. indexes that will be deleted)
        # using the last index
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        suppress = [last]
        # loop over all indexes in the indexes list
        for pos in range(0, last):
            # grab the current index
            j = idxs[pos]

            # find the largest (x, y) coordinates for the start of
            # the bounding box and the smallest (x, y) coordinates
            # for the end of the bounding box
            xx1 = max(x1[i], x1[j])
            yy1 = max(y1[i], y1[j])
            xx2 = min(x2[i], x2[j])
            yy2 = min(y2[i], y2[j])

            # compute the width and height of the bounding box
            w = max(0, xx2 - xx1 + 1)
            h = max(0, yy2 - yy1 + 1)

            # compute the ratio of overlap between the computed
            # bounding box and the bounding box in the area list
            overlap = float(w * h) / area[j]

            # if there is sufficient overlap, suppress the
            # current bounding box
            if overlap > overlapThresh:
                suppress.append(pos)

        # delete all indexes from the index list that are in the
        # suppression list
        idxs = np.delete(idxs, suppress)

    # return only the bounding boxes that were picked
    return boxes[pick]

#https://stackoverflow.com/questions/39403183/python-opencv-sorting-contours
def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[0] // tolerance_factor) * tolerance_factor) * cols + origin[1]

def get_contour_precedence_y(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

#https://stackoverflow.com/questions/38805462/how-to-sort-contours-left-to-right-while-going-top-to-bottom-using-python-and
def sort_contours_(contour):
    # initially the line bottom is set to be the bottom of the first rect
    line_bottom = contour[0][1] + contour[0][3] - 1
    line_begin_idx = 0
    for i in range(len(contour)):
        # when a new box's top is below current line's bottom
        # it's a new line
        if (contour[i][1] > line_bottom):
            # sort the previous line by their x
            contour[line_begin_idx:i] = sorted(contour[line_begin_idx:i], key=lambda b: b[0])
            line_begin_idx = i
        # regardless if it's a new line or not
        # always update the line bottom
        line_bottom = max(contour[i][1] + contour[i][3] - 1, line_bottom)
    # sort the last line
    contour[line_begin_idx:] = sorted(contour[line_begin_idx:], key=lambda b: b[0])
    return contour

def detect_text(file):
    Image=cv2.imread(file)
    I=Image.copy()
    G_Image=cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY)

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

    #Otsu Thresholding
    blur = cv2.GaussianBlur(G_Image,(1,1),0)
    ret,th = cv2.threshold(blur,0,255,cv2.THRESH_OTSU|cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # block of text
    #--- choosing the right kernel
    #--- kernel size of 3 rows (to join dots above letters 'i' and 'j')
    #--- and 10 columns to join neighboring letters in words and neighboring words
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 3))
    dilation = cv2.dilate(th, rect_kernel, iterations = 1)
     #cv2.imshow("dil", dilation)


    #---Finding contours of text block ---
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # sort contours by x and y values
    contours.sort(key=lambda y: get_contour_precedence_y(y, I.shape[1]))

    #wcnt = 0

    #wroi = np.zeros((I.shape[0], I.shape[1], I.shape[2]))
    wroi = np.zeros((I.shape[0], I.shape[1]))
    #wroi = np.full((I.shape[0], I.shape[1], I.shape[2]), 255)
    wordh = np.array([])
    wordw = np.array([])
    wordx = np.array([])
    wordy = np.array([])

    '''
    for wordcontours in contours:
            x, y, w, h = cv2.boundingRect(wordcontours)

            wordh = np.append(wordh, h)
            wordw = np.append(wordw, w)
            wordx = np.append(wordx, x)
            wordy = np.append(wordy, y)
    
    print('wordh = ', wordh)
    print('wordw = ', wordw)

    avgh = sum(wordh) / len(wordh)
    print('avgh = ', avgh)
    avgw = sum(wordw) / len(wordw)
    print('avgw = ', avgw)
    '''
    # rows = shape[0
    boxes = np.zeros((len(contours), 4))
    #print(boxes)
    bcnt = 0

    for wordcontours in contours:

        (x,y,w,h) = cv2.boundingRect(wordcontours)
        print('boundingRect = ', cv2.boundingRect(wordcontours))

        boxes[bcnt][0] = x
        boxes[bcnt][1] = y
        boxes[bcnt][2] = x + w
        boxes[bcnt][3] = y + h

        bcnt = bcnt + 1

        wordh = np.append(wordh, h)
        wordw = np.append(wordw, w)
        wordx = np.append(wordx, x)
        wordy = np.append(wordy, y)

    #print('boxes = ', boxes)

    avgh = sum(wordh) / len(wordh)
    avgw = sum(wordw) / len(wordw)

    nonover_boxes = non_max_suppression_slow(boxes, 0.3)

    print('nonover = ', nonover_boxes)

    #for boxes1 in boxes:
    for boxes1 in nonover_boxes:

        x, y, x2, y2 = boxes1

        x = int(x)
        y = int(y)
        x2 = int(x2)
        y2 = int(y2)
        '''
        print('boxes1 = ', boxes1)
        print('x', x)
        print('y', y)
        print('w', x2 - x)
        print('h', y2 - y)
        '''
        w = x2-x
        h = y2-y

        if ( (I.shape[1] * 0.98) > h > avgh - (avgh * 0.45)) and (w > avgw - (avgw * 0.65)):

            # wroi is array of 0
            # add wroi to black image for each valid wroi
            # slightly pad roi of words
            #wroi[y:y + h, x:x + w] = th[y:y + h, x:x + w]
            print(wroi.shape)
            print(th.shape)
            wroi[y:y2, x:x2] = th[y:y2, x:x2]
            #wroi[y:y2, x:x2] = I[y:y2, x:x2]

            cv2.rectangle(I, (x, y), (x2, y2), (0, 255, 0), 1)

    # save completed word roi as image
    # use later for character recognition
    cv2.imwrite(path + "\word.jpg", wroi)
    text = detect_characters(I)

    return I, text

def detect_characters(I):

    #image folder path
    imfilepath = r'C:\Users\Oikawa\Desktop\ECE5470Project\bbroi'

    # save path for characters
    path = r"C:\Users\Oikawa\Desktop\ECE5470Project\characters"

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

    ccnt = 0

    for filename in os.listdir(imfilepath):
        if filename.endswith(".jpg"):
            img = cv2.imread(imfilepath + '\\' + filename)
            gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # testing gradient after
            blur = cv2.GaussianBlur(gimg, (1, 1), 0)
            ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # sort contours by x and y values
            #contours.sort(key=lambda y: get_contour_precedence_y(y, img.shape[1]))
            contours.sort(key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * img.shape[1])
            #contours.sort(key=lambda x: get_contour_precedence(x, img.shape[0]))

            x1 = np.array([])
            y1 = np.array([])
            w1 = np.array([])
            h1 = np.array([])
            centerx = np.array([])
            centery = np.array([])

            for contour in contours:
                # get rectangle bounding contour
                [x, y, w, h] = cv2.boundingRect(contour)

                # https: // www.pyimagesearch.com / 2016 / 02 / 01 / opencv - center - of - contour /
                # get centers of rectangles
                M = cv2.moments(contour)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centerx = np.append(centerx, cx)
                centery = np.append(centery, cy)

                croi = []

                if (h > 5 and w > 3):
                    # draw rectangle around contour on original image
                    cv2.rectangle(I, (x, y), (x + w, y + h), (255, 0, 255), 0)

                    # save roi to array
                    croi = th[y - 2:y + h + 2, x - 2:x + w + 2]
                    #croi = th[y - 2:y + h + 2, x - 2:x + w + 2]

                    # https://docs.opencv.org/3.4/dc/da3/tutorial_copyMakeBorder.html
                    # pad image with black for recognition later
                    top = int(0.15 * croi.shape[0])  # shape[0] = rows
                    bottom = top
                    left = int(0.15 * croi.shape[1])  # shape[1] = cols
                    right = left
                    croi = cv2.copyMakeBorder(croi, top, bottom, left, right, cv2.BORDER_CONSTANT, None, 0)

                    # save roi as img
                    cv2.imwrite(path + "\char%d.jpg" % ccnt, croi)

                    ccnt = ccnt + 1

                    # append values
                    x1 = np.append(x1, x)
                    y1 = np.append(y1, y)
                    w1 = np.append(w1, w)
                    h1 = np.append(h1, h)

    # find difference between centers
    xdiff = np.array([])

    for i in range(1,len(centerx) - 1):
        xdiff = np.append(xdiff, centerx[i] - centerx[i-1])

    # return recognized text as string
    text = splitstring(xdiff)

    return text

def splitstring(xdiff):

    # get predicted text
    text = p.guesstext()
    try:
        # find avg of difference between centers
        # https://stackoverflow.com/questions/40295691/python-function-to-find-sum-of-positive-numbers-in-an-array
        xavg = np.sum(diff for diff in xdiff if diff > 0)/len(xdiff)
    except Exception as e:
            error = "Error"
            emessage = "No text detected\n"

            messagebox.showerror(error, emessage + "Error: " + str(e))

    # temp array to hold >0 values of distances
    tempxdif = np.array([])

    for xd in range(len(xdiff)):
        if xdiff[xd] > 0:
            tempxdif = np.append(tempxdif, xdiff[xd])

    allowdif = np.amin(tempxdif)

    # set an allowable distance
    # > allowed = space
    allowed = xavg + (allowdif * 0.45)
    # keep track of how many ' ' or '\n'
    # have been added to string
    added = 0

    # format string based on og image
    for i in range(1, len(text) - 1):
        # insert space if distance between centers is larger than acceptable
        if xdiff[i - 1] > allowed:
            # https://stackoverflow.com/questions/5254445/add-string-in-a-certain-position-in-python
            text = text[:i + added] + ' ' + text[i + added:]
            added = added + 1

        # if x distance is < 0
        # add new line
        elif xdiff[i - 1] < 0:
            text = text[:i + added] + '\n' + text[i + added:]
            added = added + 1

    return text