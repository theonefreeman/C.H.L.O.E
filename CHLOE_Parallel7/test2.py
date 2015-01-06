import cv2
import thread
import facedetect2 as fr
import colortrack as ct
import stt_final as stt
import sift as sift
import sys
from msvcrt import getch
import speech
import collections
import csv
import capture
import train
import os
import wostt

# Define a function for the thread
def vision_thread( threadName):
	print "vision thread started"
	face_rec=fr.FaceRecognize()
	colour_tracker = ct.ColourTracker()
	cv2.namedWindow("Camera_Stream", cv2.CV_WINDOW_AUTOSIZE)
	cam = cv2.VideoCapture(0)
	d = collections.deque(maxlen=100)
	mode = -1
	trained = 11
	sub_no = 1
	while 1:
		
		ret, img = cam.read()
		cont = colour_tracker.test(img)
		try:
			mode = audiomode
		except:
			print "audio thread not ready"
			continue

	
		if mode==5:                                 ##set according to speech csv file. (for "look down").
			temp = audiomode
			print "Object detection"
			speech.say("What do you want me to do?")
			print "waiting for command....\n Learn (Or) Find\n"
			while audiomode!=6 and audiomode!=7 :
				x=0
				
			
			if audiomode == 6:                        ## "learn"
			       ## TTS here to ask what object is
				flag=1
				while (flag):
					text= "What is this"
					speech.say(text)
					print "What is this?...."
					while audiomode!=0:
						x=0						

					speech.say("You said %s" %name)
					speech.say("Please confirm")
					while audiomode!=8 and audiomode!=9:
						x=0
					if audiomode==8:
					
						data = [name, trained]
						writer = csv.writer(open("mycsv.csv", "ab"), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
						writer.writerow(data)
						ret, img = cam.read()
						filename = (".\\objecttraining\\%d.jpg" % trained)
						trained+=1
						cv2.imwrite(filename, img)
						flag=0
					
				
				
			else :
				text= "Which object"
				speech.say(text)
				print "Which object?..."
				while audiomode<=10:
					x=0
				
				ret, img = cam.read()
				objID = audiomode
				filename = (".\\objecttraining\\%d.jpg" % objID)
				print filename
				template = cv2.imread(filename)
				cv2.imshow("Template", template)
				cv2.imshow("image", img)
				dist=200
				num=-1                                                          ## set accordingly!!
				skp, tkp = sift.findKeyPoints(img, template, dist)
				x , y = sift.drawKeyPoints(img, template, skp, tkp, num)
			       
				
		
		elif len(cont)>0:
			try:
				centx , centy= colour_tracker.run(img,cont)
			except:
				print "No bright objects!!"

		else:
			rects = face_rec.detect(img)
			if len(rects)!=0:
				label, x, y = face_rec.naming(img,rects)
				##print "FR index", label
				d.append(label)
				if d.count(0)>70:
					speech.say("I would like to learn about you. Please confirm")
					while audiomode!=8 and audiomode!=9:
						x=0

					if audiomode==8:
						capture.data_matrix_demo(cam)
						train.training()
						speech.say("Whats your name?")
						testVar = raw_input("Please type name...")
						data = [testVar]
						writer = csv.writer(open("names.csv", "ab"), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
						writer.writerow(data)
					
					d.clear()
					#Ask for the name
					#append to the CSV file
		
		cv2.imshow('Camera_Stream', img)
		cv2.waitKey(10)
	print "exiting vision thread"

# Define a function for the thread
def audio_thread( threadName):
	print "audio_thread started"
	stt.stt_setup()
	global audiomode
	global name
	while 1:
		audiomode, name = stt.stt_decode()
		audiomode=int(audiomode)
		print audiomode
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
