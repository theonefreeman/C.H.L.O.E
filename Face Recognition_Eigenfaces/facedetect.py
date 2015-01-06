#/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
import sys, getopt
import csv
import math
from itertools import islice

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def recognize(im):
    leastED=100;
    index=0;
    galleryfile = open( "fe.csv", "rb" )
    c=csv.reader(galleryfile)
    namefile = open( "names.csv", "rb" )
    d=csv.reader(namefile)
    im = cv2.resize(im, (300,300))
    im = cv2.pyrDown(im)
    im = cv2.cvtColor( im, cv2.COLOR_RGB2GRAY )
    im= cv2.equalizeHist(im)
    im = np.float32(im)/255.0       # float conversion/scale
    dst = cv2.dct(im)               # the dct    
    im2 = im[1:30, 1:30]
    out = im2.ravel()
    out = out.astype(np.float)
    for row in c:
        index += 1
        row = np.asarray(row)
        row = row.astype(np.float)
        temp1 = np.subtract(out,row)
        temp1 = np.square(temp1)
        ED = math.sqrt(float(sum(temp1)))
        if ED<leastED:
            leastED=ED
            match=index
    match=int(match/5+1)
    name = list(islice(d,match))[-1]
    galleryfile.close()
    namefile.close()
    return name

if __name__ == '__main__':
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)

    cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        #t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        if len(rects)!=0:
            print rects,len(rects)
            for i in rects:
                x1=i[0]
                y1=i[1]
                x2=i[2]
                y2=i[3]
                
                bridgex1 = x1+(x2-x1)/2
                bridgey1 = y1+(y2-y1)/3
                
                cv2.circle(vis, (bridgex1, bridgey1), 3, (0, 255, 0), -1)
                face1=img[x1:x2,y1:y2]
                
                name1 = recognize(face1)
               
                cv2.putText(vis, str(name1),(x1,y1),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255))
                print name1
                
                        
        draw_rects(vis, rects, (0, 255, 0))
        #dt = clock() - t

        #draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()

