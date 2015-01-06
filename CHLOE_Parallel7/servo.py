import serial
import time
import math
import csv
from itertools import islice

class servo:
	def __init__(self):
		self.ser = serial.Serial("COM20", 9600)
		time.sleep(2)

	def send(self,channel,angle,speed):
		self.ser.write(chr(channel))
		self.ser.write(chr(angle))
		self.ser.write(chr(speed))
		time.sleep(0.1)
		#tdata = self.ser.readline()

	def end(self):
		self.ser.close()

	def mapi(self,x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

	def track(self,x,y):
		if x<150:
			diff=150-x
			val=self.mapi(diff,0,150,103,130)
			self.send(5,val,1)
		elif x>490:
			diff=x-490
			val=self.mapi(diff,0,150,103,70)
			self.send(5,val,1)
		elif y<110:
			diff=110-y
			val=self.mapi(diff,0,110,75,25)
			self.send(4,val,1)
		elif y>320:
			diff=y-370
			val=self.mapi(diff,0,110,75,90)
			self.send(4,val,1)
		else:
			self.send(0,self.mapi(x,100,540,60,120),1)
			self.send(1,self.mapi(y,70,410,50,120),1)
			self.send(2,self.mapi(y,70,410,110,60),1)
			self.send(3,self.mapi(x,100,540,60,130),1)

	def pointto(self,x,y):
                gridno=4*(math.ceil(y/120))+math.ceil(x/160)+1
                print math.ceil(y/120)
                print math.ceil(x/160)
                print gridno
                d=csv.reader(open("servo.csv", "r" ))
                values = list(islice(d,gridno))[-1]
                self.send(6,int(values[0]),1)
                self.send(7,int(values[1]),1)
                self.send(8,int(values[2]),1)
                self.send(9,int(values[3]),1)
                self.send(10,int(values[4]),1)
                self.send(11,int(values[5]),1)
                self.send(12,int(values[6]),1)
                self.send(13,int(values[7]),1)

        def default(self):
                self.send(0,90,1)
                self.send(1,75,1)
                self.send(14,90,1)
                self.send(3,100,1)
                self.send(4,75,1)
                self.send(5,103,1)
                self.send(6,0,1)
                self.send(7,140,1)
                self.send(8,110,1)
                self.send(9,70,1)
                self.send(10,150,1)
                self.send(11,0,1)
                self.send(12,180,1)
                self.send(13,170,1)
                
                
