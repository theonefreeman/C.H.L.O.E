#/usr/bin/env python

'''
Keyboard shortcuts:

   q or ESC - exit
   space - save current image as datamatrix<frame_number>.jpg
'''

import cv2
import cv2.cv as cv
import numpy as np
import sys
import os
import getopt

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def data_matrix_demo(cap):
    window_name = "Data Matrix Detector"
    frame_number = 0
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    sub_no = len(os.listdir('training'))
    sub_no += 1
    os.chdir('training')
    os.mkdir('%d' % sub_no)
    os.chdir('..')
    

    while 1:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        codes, corners, dmtx = cv2.findDataMatrix(gray)

        cv2.drawDataMatrixCodes(frame, codes, corners)
        cv2.imshow(window_name, frame)
        gray = cv2.equalizeHist(gray)
        rects = detect(gray, cascade)

        key = cv2.waitKey(1000)
        # c = chr(key & 255)
        # if c in ['q', 'Q', chr(27)]:
        #     break

        if len(rects)!=0:
            x1=rects.item(0)
            y1=rects.item(1)
            x2=rects.item(2)
            y2=rects.item(3)
            crop_img = gray[y1:y2, x1:x2]
            #cv2.imshow('face', crop_img)
            filename = ("datamatrix%03d.jpg" % frame_number)
            os.chdir('training\\%s' % str(sub_no))
            cv2.imwrite(filename, crop_img)
            os.chdir('..')
            os.chdir('..')
            print "Saved frame to " + filename
            frame_number += 1
            if frame_number == 10:
                break
    


# def main():

#     if len(sys.argv) == 1:
#         cap = cv2.VideoCapture(0)
#     else:
#         cap = cv2.VideoCapture(sys.argv[1])
#         if not cap.isOpened():
#             cap = cv2.VideoCapture(int(sys.argv[1]))

#     if not cap.isOpened():
#         print 'Cannot initialize video capture'
#         sys.exit(-1)

#     data_matrix_demo(cap)
#     cv2.destroyAllWindows()
#     cap.release()
