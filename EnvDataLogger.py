#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# EnvDataLogger.py
# Copyright (c) 2017 Henning Kerstan.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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

# print start message and create new file
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
