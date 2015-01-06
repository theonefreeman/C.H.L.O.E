import cv2
import thread
import facedetect2 as fr
import colortrack as ct
import stt_final as stt
from msvcrt import getch
import sys
import collections
import capture
import train

# Define a function for the thread
def vision_thread( threadName):
 	print "vision thread started"
 	face_rec=fr.FaceRecognize()
  	colour_tracker = ct.ColourTracker()
  	cv2.namedWindow("Camera_Stream", cv2.CV_WINDOW_AUTOSIZE)
  	cam = cv2.VideoCapture(0)
  	d = collections.deque(maxlen=100)
   	while 1:
   		ret, img = cam.read()
		cont = colour_tracker.test(img)
		if len(cont)>0:
			colour_tracker.run(img,cont)
		else:
			rects = face_rec.detect(img)
			if len(rects)!=0:
				label = face_rec.naming(img,rects)
				print "FR index", label
				d.append(label)
				if d.count(0)>70:
					#Ask confirmation if it has to learn
					capture.data_matrix_demo(cam)
					train.training()
					d.clear()
					#Ask for the name
					#append to the CSV file
		cv2.imshow('Camera_Stream', img)

		# try:
		# 	print mode
		# except:
		# 	print "audio thread not running"

		cv2.waitKey(5)
   	print "exiting vision thread"

# Define a function for the thread
def audio_thread( threadName):
	print "audio_thread started"
	stt.stt_setup()
	global mode
	while 1:
		mode = stt.stt_decode()
		print "audio index", mode
	print "exiting audio thread"

if __name__ == '__main__':
	# Create two threads as follows
	try:
   		thread.start_new_thread( vision_thread, ("vision",  )  )
   		thread.start_new_thread( audio_thread, ("audio",  )  )
	except:
   		print "Error: unable to start thread"

	while 1:
		key = ord(getch())
		if key == 27:
			thread.exit()
			sys.exit()
