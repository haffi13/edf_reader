import datetime
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys
import math

basestring = r'C:\ProjectResources'
filename = '5.edf'  # The 5.edf file is lacking some of the properties an edf file can have, should use some other file for testing

ANNOTATIONS = 'EDF Annotations'


class EdfEndOfData(BaseException):
    pass


class HeaderReader:
    def __init__(self, file):
        self.file = file  # Change this to call the function instead ?

    def read_header(self):
        self.header = get_header_data(self.file)  # Move to init? google
        self.dig_min, self.phys_min, self.phys_range, self.dig_range, self.gain = get_other_header_values(self.header)

    def read_raw_record(self):
        result = []
        for num_samples in self.header['number_of_samples_per_record']:
            samples = self.file.read(num_samples * 2)
            if len(samples) != num_samples * 2:
                raise EdfEndOfData  # Find potential solutions that don't require raising an exception.
            result.append(samples)
        return result

    def convert_record(self, record):
        h = self.header
        dig_min, phys_min, gain = self.dig_min, self.phys_min, self.gain
        time = float('nan')
        signals = []
        events = []
        for i, samples in enumerate(record):
            if h['label'][i] == ANNOTATIONS:
                ann = get_tal(samples)
                time = ann[0]
                events.extend(ann[1:])
            else:
                dig = np.frombuffer(samples, '<i2').astype(float)  #
                phys = (dig - dig_min[i]) * gain[i] + phys_min[i]
                signals.append(phys)
        return time, signals, events

    def read_record(self):
        return self.convert_record(self.read_raw_record())

    def records(self):
        '''
        Record generator.
        '''
        try:
            while True:
                yield self.read_record()
        except EdfEndOfData:
            pass


# tal = Time-stamped Annotations Lists
def get_tal(tal_bytes):
    exp = br'(?P<onset>[+\-][0-9]+(?:\.[0-9]*)?)' + \
          br'(?:\x15(?P<duration>[0-9]+(?:\.[0-9]*)?))?' + \
          br'(\x14(?P<annotation>[^\x00]*))?' + \
          br'(?:\x14\x00)'

    def annotation_to_list(annotation):
        return str(annotation, 'utf-8').split('\x14') if annotation else []

    def parse(dic):
        return (
            float(dic['onset']),
            float(dic['duration']) if dic['duration'] else 0.,
            annotation_to_list(dic['annotation']))

    return [parse(m.groupdict()) for m in re.finditer(exp, tal_bytes)]


def get_other_header_values(header):
    dmin = header['digital_minimum']
    pmin = header['physical_minimum']
    pran = get_range(header['physical_maximum'], pmin)
    dran = get_range(header['digital_maximum'], dmin)
    gain = get_gain(pran, dran)
    return dmin, pmin, pran, dran, gain


def get_range(max_value, min_value):
    range = []
    for ma, mi in zip(max_value, min_value):
        range.append(ma - mi)
    return range


def get_gain(phys_range, dig_range):
    ret = []
    for phys, dig in zip(phys_range, dig_range):
        ret.append(phys / dig)
    return ret


def load_edf_file(edffile):
    if isinstance(edffile, str):
        os.chdir(basestring)  # <---------- Use os.path instead of hardcoding.
        with open(edffile, 'rb') as edf:
            return load_edf_file(edf)
    reader = HeaderReader(edffile)
    reader.read_header()
    rectime, data_points, annotations = list(zip(*reader.records()))

    i = 0
    length = len(data_points)
    sinewave = np.empty([0, 0])
    print('------------------------------------------------------------------------------------------')
    while i < length:
        t = data_points[i][5]
        i += 1
        sinewave = np.append(sinewave, t)
    print(len(sinewave))
    print(type(sinewave))
    sinemax = math.ceil(np.amax(sinewave))
    sinemin = math.floor(np.amin(sinewave))
    print('sinemax - ' + str(sinemax))
    print('sinemin - ' + str(sinemin))
    smin = sys.float_info.max
    smax = sys.float_info.min
    print(smin)
    print(smax)
    s = ''
    for x in sinewave:
        s += str(type(x))
        s += ' - '
    with open('type_result.txt', 'w') as wf:
        wf.write(s)
        print('file created!')
    print('min = ' + str(smin) + '   max = ' + str(smax))

    fig, ax = plt.subplots()
    t = np.arange(0.0, 600.00, 0.005)  # (0, number of records, (number_of_records / number_of_records * sampling rate))
    print(len(t))
    plt.plot(t, sinewave)
    plt.axis([0, 10, sinemin, sinemax])  # first 2 numbers are range that is visible at a time, last 2 are min/max for y axis
    axpos = plt.axes([0.2, 0.1, 0.65, 0.03])  # position of the slider bar
    spos = Slider(axpos, 'Pos', 0.1, 590)  # position, label, step size, length(max - visible range at a time)

    def update(val):
        pos = spos.val
        ax.axis([pos, pos + 10, sinemin, sinemax])  # bottom_left_pos, pos+visible range at a time, min/max for y axis
        fig.canvas.draw_idle()

    spos.on_changed(update)
    ax.grid(True)
    plt.show()

    return reader.header  # The return values of this method cannot be changed without breaking tests.
    # 'b' prefix in front of string means it's a bytes literal
    # Maybe it doesn't matter, otherwise just cast to string in get_header_data


def get_header_data(f):
    h = {}
    # Here we should make sure that the file is the correct type before proceeding
    # fx. assert file.read(8) == '0       '
    # 'edf+c' => uninterrupted(contiguous) recording && 'edf+d' => interrupted recording
    h['data_format_version'] = f.read(8).decode('ascii').strip()
    h['local_patient_id'] = f.read(80).decode('ascii').strip()
    h['local_recording_id'] = f.read(80).decode('ascii').strip()
    h['start_time'] = get_start_time(f.read(8).decode('ascii'), f.read(8).decode('ascii'))
    h['bytes_in_header'] = int(f.read(8))
    h['subtype'] = f.read(44).decode('ascii').strip()
    h['contiguous'] = contiguity(h['subtype'])
    h['number_of_records'] = int(f.read(8))
    h['record_duration'] = float(f.read(8))
    ns = h['number_of_signals'] = int(f.read(4))  # ns - variable for use when reading the data

    channels = range(ns)  # Creates a list of numbers used for iteration in the for-loops below
    h['label'] = [f.read(16).decode('ascii').strip() for n in channels]
    h['transducer_type'] = [f.read(80).decode('ascii').strip() for n in channels]
    h['physical_dimension'] = [f.read(8).decode('ascii').strip() for n in channels]
    h['physical_minimum'] = [float(f.read(8)) for n in channels]
    h['physical_maximum'] = [float(f.read(8)) for n in channels]
    h['digital_minimum'] = [float(f.read(8)) for n in channels]
    h['digital_maximum'] = [float(f.read(8)) for n in channels]
    h['prefiltering'] = [f.read(80).decode('ascii').strip() for n in channels]
    h['number_of_samples_per_record'] = [int(f.read(8)) for n in channels]
    h['reserved'] = [f.read(32) for n in channels]
    return h


def contiguity(subtype):
    if subtype == 'EDF+D':
        return False
    return True


def get_start_time(date, time):
    day, month, year = [int(x) for x in re.findall('([0-9][0-9])', date)]
    hour, minute, sec = [int(x) for x in re.findall('([0-9][0-9])', time)]
    return str(datetime.datetime(2000 + year, month, day, hour, minute, sec))
