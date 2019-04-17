# import libraries
import cv2
import os

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

    #cv2.imshow("thresh",th)
    # sort contours by x and y values
    contours.sort(key=lambda y:get_contour_precedence_y(y, I.shape[1]))

    #individual characters bounding boxes
    cnt = 0

    for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            roi = []

            if (h>=0) :

                # draw rectangle around contour on original image
                cv2.rectangle(I, (x, y), (x + w, y + h), (255, 0, 255), 0)

                # save roi to array
                roi = th[y:y + h, x:x + w]
                #save roi as img
                cv2.imwrite( path + "\char%d.jpg" % cnt, roi)

                cnt = cnt + 1


    # block of text
    #--- choosing the right kernel
    #--- kernel size of 3 rows (to join dots above letters 'i' and 'j')
    #--- and 10 columns to join neighboring letters in words and neighboring words
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
    dilation = cv2.dilate(th, rect_kernel, iterations = 1)
    #cv2.imshow("dil", dilation)

    #---Finding contours of text block ---
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(I, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imshow("i", I)

    return I