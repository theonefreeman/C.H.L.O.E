#/usr/bin/env python

'''
    Training has begun
'''

import cv2.cv as cv
import cv2
import numpy as np
import csv
import os

if __name__ == '__main__':
    print __doc__
    frame_number = 0
    csvfile = open( "fe.csv", "ab" )
    c=csv.writer(csvfile)
    sub_no = len(os.listdir('Database'))
    os.chdir('Database\\'+str(sub_no))
    
    for x in xrange(1,6):
        im = cv2.imread("datamatrix%03d.jpg" % frame_number)
        im = cv2.resize(im, (300,300))
        im = cv2.pyrDown(im)
        im = cv2.cvtColor( im, cv2.COLOR_RGB2GRAY )
        im= cv2.equalizeHist(im)
        im = np.float32(im)/255.0       # float conversion/scale
        dst = cv2.dct(im)               # the dct
        #im = np.uint8(dst)*255.0        # convert back
        im2 = im[1:30, 1:30]
        out = im2.ravel()
        c.writerow(out)
        cv2.imshow('org', im)
        #cv2.imshow('out', out)
        #cv2.imwrite('out.jpg', im)
        print out
        frame_number += 1
        cv2.waitKey()
        
    csvfile.close()
    cv2.destroyAllWindows()
