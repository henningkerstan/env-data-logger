#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Henning Kerstan.

import sys
import Adafruit_DHT
import time
import datetime

# set logging path
path = '/srv/smbshares/envdata/'

# set sensor model and GPIO pin
sensor = Adafruit_DHT.DHT22
pin = 4

# set log interval (in minutes)
interval = 5

# function to create new log file with current date & time as filename
def create_new_file():
    filename = path + time.strftime("%Y-%m-%d") + "_" + time.strftime("%H-%M") + "_envdata.csv" 
    f = open(filename, 'w')
    headerrow="Date,Time,Temperature [°C],Humidity [%]"
    f.write(headerrow+"\n")
    f.close
    print("New log file: " + filename)
    return filename



print("Log interval: " + str(interval) + " minutes")
filename = create_new_file()


# the minute of the previous measurement
prev_minute = 60

# main program loop
while 1==1:

    # check if is time for a new measurement
    now = datetime.datetime.now()
    if (now.minute % interval == 0) and (now.minute != prev_minute):
        prev_minute = now.minute
        
        # check if a new file needs to be created (new day)
        if (now.hour == 0) and (now.minute == 0):
            filename = create_new_file()
    
        # read date from sensor and write to file if successful
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            datarow=time.strftime("%Y-%m-%d") + "," + time.strftime("%H:%M") + ',{0:0.1f},{1:0.1f}'.format(temperature, humidity)
            f = open(filename, 'a')
            print(datarow)
            f.write(datarow+"\n")
            f.close()
    
    # sleep for 10 seconds
    time.sleep(10)


sys.exit(0)