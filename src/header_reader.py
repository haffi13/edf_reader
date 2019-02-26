import datetime
import os
import re

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
        self.dig_min, self.phys_min, self.phys_range, self.dig_range, self.gain = get_some_values(self.header)

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
        signal = []
        events = []
        for i, samples in enumerate(record):
            print('debug: h[label] == ' + str(h['label'][i]))
            print(h['label'])
            if h['label'][i] == ANNOTATIONS:
                #need to write annnotation function
                break




def get_some_values(header):
    dmin = header['digital_minimum']
    pmin = header['physical_minimum']
    pran = get_range(header['physical_maximum'], pmin)
    dran = get_range(header['digital_maximum'], dmin)
    gain = get_gain(pran, dran)
    return dmin, pmin, pran, dran, gain


def get_range(max_value, min_value):
    ret = []
    for ma, mi in zip(max_value, min_value):
        ret.append(ma - mi)
    return ret


def get_gain(phys_range, dig_range):
    ret = []
    for phys, dig in zip(phys_range, dig_range):
        ret.append(phys / dig)
    return ret


def load_edf_file(edffile):
    if isinstance(edffile, str):
        os.chdir(basestring)
        with open(edffile, 'rb') as edf:
            return load_edf_file(edf)

    reader = HeaderReader(edffile)
    reader.read_header()
    rec = reader.read_raw_record()
    print('rec    ->    ' + str(rec))
    print('!!! RECSTART !!!')
    print(rec)
    print('!!! RECOVER !!!')
    # h = reader.header
    return reader.header
    # 'b' prefix in front of string means it's a bytes literal
    # Maybe it doesn't matter, otherwise just cast to string in get_header_data

    print('DataFormatVersion - ' + str(h['data_format_version']))
    print(h['data_format_version'])
    print('LocalPatientId - ' + str(h['local_patient_id']))
    print(h['start_time'])
    print('bytes in header - ' + str(h['bytes_in_header']))
    print('subtype - ' + str(h['subtype']))
    print('contiguous - ' + str(h['contiguous']))
    print('num of records - ' + str(h['number_of_records']))
    print('record duration - ' + str(h['record_duration']))
    print('num of signals - ' + str(h['number_of_signals']))
    print('label ' + str(h['label']))
    print(h['transducer_type'])
    print(h['physical_dimension'])
    print(h['physical_minimum'])
    print(h['physical_maximum'])
    print(h['digital_minimum'])
    print(h['digital_maximum'])
    print(h['prefiltering'])
    print(h['number_of_samples_per_record'])
    print(h['reserved'])


def get_header_data(f):
    h = {}
    # Here we should make sure that the file is the correct type before proceeding
    # fx. assert file.read(8) == '0       '   <-- find out if the value can be anything other than 0
    # 'edf+c' => uninterrupted(contiguous) recording && 'edf+d' => interrupted recording
    # h['contiguous'] = h['subtype'] != 'EDF+D'
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

    channels = range(ns)
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
    (day, month, year) = [int(x) for x in re.findall('([0-9][0-9])', date)]
    (hour, minute, sec) = [int(x) for x in re.findall('([0-9][0-9])', time)]
    return str(datetime.datetime(2000 + year, month, day, hour, minute, sec))
