#!/usr/bin/python
import time
import datetime
import RPi.GPIO as GPIO
import urllib
import hashlib

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)  # Red
GPIO.setup(18, GPIO.OUT)  # Green
GPIO.setup(27, GPIO.OUT)  # Yellow
GPIO.setup(22, GPIO.OUT)  # Sound

state = 0
LastState = -1
getready = 60
curr = time.time()
learningTime = 3000
pauseTime = 600


def ChangeState():
    global curr
    global state
    if (state == 0 and LastState == -1) or (state == 0 and LastState != -1 and curr + learningTime < time.time()):
        state = 1
        curr = time.time()
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.HIGH)
        SoundTemplates(1)
    elif (state == 1 and LastState == -1) or (state == 1 and LastState != -1 and curr + pauseTime < time.time()):
        state = 0
        curr = time.time()
        GPIO.output(18, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)
        SoundTemplates(2)


def CheckIfTimesRunningOut():
    global curr
    global getready
    global state
    global learningTime
    global pauseTime
    if state == 0 and curr + learningTime - time.time() < getready:
        return True
    elif state == 1 and curr + pauseTime - time.time() < getready:
        return True
    else:
        return False


def SoundTemplates(template):
    if template == 1:
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(22, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(22, GPIO.LOW)
    elif template == 2:
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(22, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(22, GPIO.LOW)


def Program():
    global curr
    global pauseTime
    global learningTime
    global getready
    global LastState
    ChangeState()
    if CheckIfTimesRunningOut():
        time.sleep(0.5)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(27, GPIO.LOW)
    if state != LastState:
        LastState = state
        if state == 0:
            print "[" + datetime.datetime.fromtimestamp(curr).strftime('%Y-%m-%d %H:%M:%S') + "] Tanulas in progress.."
        elif state == 1:
            print "[" + datetime.datetime.fromtimestamp(curr).strftime('%Y-%m-%d %H:%M:%S') + "] Szunet in progress.."


try:
    print "==== Tanulas koordinalo v1.0 ===="
    while True:
        Program()
except KeyboardInterrupt:
    GPIO.cleanup()
    print "\Megszakitva"
