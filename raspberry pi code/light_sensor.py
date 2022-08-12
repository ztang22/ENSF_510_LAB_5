# code by chris-gong source from https://github.com/chris-gong/forty-yard-dash-rpi/blob/master/photoResistorTest.py
import RPi.GPIO as GPIO
import time
import csv
file = "light.csv"
GPIO.setmode(GPIO.BCM)

resistorPin = 14

def fet_data():
    GPIO.setup(resistorPin, GPIO.OUT)
    GPIO.output(resistorPin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN)
    currentTime = time.time()
    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW):
        diff  = time.time() - currentTime
        
    data1 = diff * 1000
    print("Photo_resistance:{}".format(data1))
    return data1


if __name__ == "__main__":
    while True:
        data1= fet_data()
        time_str = time.ctime()
        with open(file,'a') as f:
            writer = csv.writer(f)
            writer.writerow([data1, time_str])
        time.sleep(60)



