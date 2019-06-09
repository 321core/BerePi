## Crate by TJ

import serial,os,time
import sys
import RPi.GPIO as GPIO
import picamera
import subprocess
import datetime
import os

# check pin location
gled = 19
rled = 26

# HW setup, GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(rled, GPIO.OUT)
GPIO.setup(gled, GPIO.OUT)
time.sleep(1)

def ledr_on():
  GPIO.output(rled, True)
def ledr_off():
  GPIO.output(rled, False)
def ledg_on():
  GPIO.output(gled, True)
def ledg_off():
  GPIO.output(gled, False)

# init LED OFF
ledr_off()
ledg_off()
time.sleep(1)

with picamera.PiCamera() as camera:

  while True:
    camera.start_preview()
    ledg_on()

    camera.capture('./now.jpg')
    camera.stop_preview()

    result = subprocess.check_output(['./darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights now.jpg'], shell=True)
    percent = result.find("person")
    if percent > 0 : # Person Key word OK
      f_percent = float(result[percent+8:-2])
      if f_percent > 80 :
        print "Person OK"
        now =  datetime.datetime.now()
        nowdatetime = now.strftime('%Y-%m-%d_%H:%M:%S')
        cmd = 'cp -f now.jpg ./screenshot/'+nowdatetime+'.jpg'
        print cmd
        os.system(cmd)
        #time.sleep(10)
      else :
        print "Person None"
        #time.sleep(10)
    else :
      print "Person None"
    time.sleep(10)

  ledg_off()

GPIO.cleanup()
