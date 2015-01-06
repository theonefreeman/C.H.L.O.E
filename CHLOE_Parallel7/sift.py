import cv2
import numpy as np
import itertools
import sys


def findKeyPoints(img, template, distance=200):
    detector = cv2.FeatureDetector_create("SIFT")
    descriptor = cv2.DescriptorExtractor_create("SIFT")

    skp = detector.detect(img)
    skp, sd = descriptor.compute(img, skp)

    tkp = detector.detect(template)
    tkp, td = descriptor.compute(template, tkp)

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(sd, flann_params)
    idx, dist = flann.knnSearch(td, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    skp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            skp_final.append(skp[i])

    flann = cv2.flann_Index(td, flann_params)
    idx, dist = flann.knnSearch(sd, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    tkp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            tkp_final.append(tkp[i])

##    print skp_final
##    print "wait"
##    print tkp_final
    return skp_final, tkp_final

def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
        c=[0 for i in range(num)]
        d=[0 for i in range(num)]
    for i in range(num):
##        a[i]=int(tkp[i].pt[0])
##        b[i]=int(tkp[i].pt[1]+hdif)
        c[i]=int(skp[i].pt[0]+w2)
        d[i]=int(skp[i].pt[1])
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
##        print pt_a
##        print pt_b
        cv2.line(newimg, pt_a, pt_b, (255, 20, 10))
    pt_c=(min(c),max(d))
    pt_d=(max(c),min(d))
    cv2.rectangle(newimg, pt_c, pt_d, (0, 0, 255),3)
    pt_c=int(sum(c) / float(len(c)))
    pt_d=int(sum(d) / float(len(d)))
    cv2.circle(newimg, (pt_c, pt_d), 1, (0, 0, 255),3)
    return pt_c, pt_d


def match():
    img = cv2.imread("img3.jpg")
    temp = cv2.imread("img4.jpg")
    try:
    	dist = int(sys.argv[3])
    except IndexError:
    	dist = 200
    try:
    	num = int(sys.argv[4])
    except IndexError:
    	num = -1
    print dist
    skp, tkp = findKeyPoints(img, temp, dist)
    newimg = drawKeyPoints(img, temp, skp, tkp, num)
    cv2.imwrite("test7.jpg", newimg)
    cv2.waitKey(0)
    
