import cv2
import thread
import facedetect2 as fr
import colortrack as ct
import stt_final as stt

# Define a function for the thread
def vision_thread( threadName):
 	print "vision thread started"
 	face_rec=fr.FaceRecognize()
        colour_tracker = ct.ColourTracker()
  	cv2.namedWindow("Camera_Stream", cv2.CV_WINDOW_AUTOSIZE)
  	cam = cv2.VideoCapture(0)
   	while 1:
   		ret, img = cam.read()
		cont = colour_tracker.test(img)
		if len(cont)>0:
			colour_tracker.run(img,cont)
		else:
			rects = face_rec.detect(img)
			if len(rects)!=0:
				face_rec.naming(img,rects)
		cv2.imshow('Camera_Stream', img)
		cv2.waitKey(10)
   	print "exiting vision thread"

# Define a function for the thread
def audio_thread( threadName):
	print "audio_thread started"
	stt.stt_setup()
	while 1:
		mode = stt.stt_decode()
		print mode
	print "exiting audio thread"

# Create two threads as follows
try:
   thread.start_new_thread( vision_thread, ("vision",  )  )

   thread.start_new_thread( audio_thread, ("audio",  )  )
except:
   print "Error: unable to start thread"

while 1:
	if 0xFF & cv2.waitKey(5) == 27:
		break;
