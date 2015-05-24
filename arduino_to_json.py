#!/usr/bin/python

import json
import os.path
import time
from temperature_interface import TemperatureInterface


def temperature_sample_to_json(today, now, temperature):
    entry = {
        "date": today,
        "time": now,
        "temperature": temperature,
    }
    return entry


def get_today_string():
    localtime = time.localtime()
    today = time.strftime("%Y-%m-%d", localtime)
    return today

config = {
    'arduino_serial_port': '/dev/cu.usbmodem621',
    'sample_interval': 0,
}

if __name__ == '__main__':
    with TemperatureInterface(config['arduino_serial_port']) as arduino:
        data = []

        today_str = get_today_string()
        filename = 'temperature_' + today_str + '.json'

        # create file if it does not exists
        if not os.path.isfile(filename):
            with open(filename, "w") as newfile:
                newfile.write('[]')

        while True:
            # get current data
            with open(filename, "r") as datafile:
                data = json.load(datafile)
                print data

            # request a new sample
            arduino.request_new_sample()

            # prepare date
            localtime = time.localtime()
            today = time.strftime("%Y-%m-%d", localtime)
            now = time.strftime("%H:%M:%S", localtime)
            # retrieve the sample
            sample = arduino.retrieve_new_sample()

            # put the sample in json format to the current data
            data.append(temperature_sample_to_json(today, now, sample))

            # write it back to the file
            with open(filename, "w") as datafile:
                parseable_data = json.dumps(data)
                datafile.write(parseable_data)

            # wait before requesting a new sample
            time.sleep(config['sample_interval'])
