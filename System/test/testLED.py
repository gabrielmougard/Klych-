import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

GPIO.output(22,GPIO.HIGH)
time.sleep(3)
GPIO.output(23,GPIO.HIGH)
time.sleep(3)
GPIO.output(24,GPIO.HIGH)
time.sleep(3)
GPIO.output(27,GPIO.HIGH)
time.sleep(3)
GPIO.output(22,GPIO.LOW)
time.sleep(3)
GPIO.output(23,GPIO.LOW)
time.sleep(3)
GPIO.output(24,GPIO.LOW)
time.sleep(3)
GPIO.output(27,GPIO.LOW)
time.sleep(3)
