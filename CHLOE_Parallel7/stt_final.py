import pyaudio
import wave
import audioop
from collections import deque 
import os
import urllib2
import urllib
import time
import csv

def stt_setup():
     #config
    global chunk
    global FORMAT
    global CHANNELS
    global RATE
    global THRESHOLD
    global SILENCE_LIMIT
    global FLAC_CONV
    global rel
    global slid_win
    global started

    chunk = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    THRESHOLD = 100 #The threshold intensity that defines silence signal (lower than).
    SILENCE_LIMIT = 2 #Silence limit in seconds. The max ammount of seconds where only silence is recorded. When this time passes the recording finishes and the file is delivered.
    FLAC_CONV = 'flac -f ' # We need a WAV to FLAC converter.\
    
    
    

def stt_decode():
    #open stream
    p = pyaudio.PyAudio() 
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    print "* listening. CTRL+C to finish."
    all_m = []
    data = ''
    rel = RATE/chunk
    slid_win = deque(maxlen=SILENCE_LIMIT*rel)
    started = False
    i=1
    while (i<2):
        data = stream.read(chunk)
        slid_win.append (abs(audioop.avg(data, 2)))

        if(True in [ x>THRESHOLD for x in slid_win]):
            if(not started):
                print "starting record"
            started = True
            all_m.append(data)
        elif (started==True):
            print "finished"
            #the limit was reached, finish capture and deliver
            filename = 'output_'+str(int(time.time()))


            # write data to WAV file
            data = ''.join(all_m)
            wf = wave.open(filename+'.wav', 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(data)
            wf.close()
            #print filename


            #Convert to flac
            os.system(FLAC_CONV+ filename+'.wav')
            f = open(filename+'.flac','rb')
            flac_cont = f.read()
            f.close()
            

            #post it
            lang_code='en-IN'
            googl_speech_url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'
            hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",'Content-type': 'audio/x-flac; rate=16000'}
            req = urllib2.Request(googl_speech_url, data=flac_cont, headers=hrs)
            try:
                p = urllib2.urlopen(req)
                c=0
    
                data= (p.read()).split('transcript\":\"')[1]
                res= data.split('"')[0]
                map(os.remove, (filename+'.flac', filename+'.wav'))
                print res
                name= res
                with open('mycsv.csv', 'rt') as f:
                 reader = csv.reader(f, delimiter=',')
                 for row in reader:
                    for field in row:
                        if field == res:
                            a,b = row
                            #print 'mode= ', b
                            c=1
                if c==0:
                    b=0
                    #print 'mode= ', b
        


            except:
                b=-1
                try:
                    os.remove(filename+'.flac')
                    os.remove(filename+'.wav')
                except:
                    print "no such file"
                #print 'mode= ', b
                res = None
                name= ""
                #print "I Can't Recognize"
   
            #reset all
            return (b, name)
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT*rel)
            all_m= []
            i=i+1

    print "* done recording"
    stream.close()
    #p.terminate()
