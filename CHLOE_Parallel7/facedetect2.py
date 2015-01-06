#/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
import csv
import math
from itertools import islice
import config

class FaceRecognize:
    """docstring for FaceRecognize"""
    def __init__(self):
        self.model = cv2.createEigenFaceRecognizer()
        self.cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        self.model = cv2.createEigenFaceRecognizer()
        self.model.load(config.TRAINING_FILE)
        
    def detect(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.gray = cv2.equalizeHist(gray)
        rects = self.cascade.detectMultiScale(self.gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

    def naming(self,img,rects):
        least_label=100
        for x1,y1,x2,y2 in rects:
            namefile = open( "names.csv", "rb" )
            d=csv.reader(namefile)
            bridgex = x1+(x2-x1)/2
            bridgey = y1+(y2-y1)/3
            cv2.circle(img, (bridgex, bridgey), 3, (0, 255, 0), -1)
            face=self.gray[x1:x2,y1:y2]
            height,width=face.shape
            if height!=0 and width!=0:
                face = cv2.resize(face, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
                label = self.recognize(face)
                #print label
                if label:
                    name = list(islice(d,label))[-1]
                else:
                    label = 0
                    name = "new"
                cv2.putText(img, str(name),(x1,y1),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255))
                if label<=least_label:
                    least_label = label
                    posx = bridgex
                    posy = bridgey
                #print name
            self.draw_rects(img, rects, (0, 255, 0))
            namefile.close()
            return least_label, bridgex, bridgey

    def draw_rects(self,img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    def recognize(self,im):
        label, confidence = self.model.predict(im)
        print confidence
        if confidence < config.POSITIVE_THRESHOLD:
            #print 'Recognized face!'
            return label
# if __name__ == '__main__':

#     face_rec=FaceRecognize()
#     cv2.namedWindow("facedetect", cv2.CV_WINDOW_AUTOSIZE)
#     cam = cv2.VideoCapture(1)

#     while True:
#         ret, img = cam.read()
#         rects = face_rec.detect(img)
#         if len(rects)!=0:
#             face_rec.naming(img,rects)  

#         cv2.imshow('facedetect', img)
#         #cv2.waitKey()
#         if 0xFF & cv2.waitKey(5) == 27:
#             break
#     cv2.destroyAllWindows()
