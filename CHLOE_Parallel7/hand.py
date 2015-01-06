import servo
import speech
import time


if __name__ == '__main__':
    motor=servo.servo()
    count = 2
    string1= "Hello!"
    motor.send(6,140,2)
    time.sleep(3)
    speech.say(string1)
    while count>=0:
        print "working"
        motor.send(8,140,3)
        motor.send(9,30,3)
        time.sleep(1)
        motor.send(8,70,3)
        motor.send(9,70,3)
        time.sleep(1)
        count=count-1

    string2 = "My Name is Chloe. I am an online embodiment of a cognitive system."
    motor.send(6,0,2)
    motor.send(8,110,2)
    motor.send(9,70,2)
    speech.say(string2)
    motor.end()
    


    
    
