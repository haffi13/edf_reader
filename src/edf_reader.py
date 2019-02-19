import datetime
import os
import re

basestring = r'C:\ProjectResources'
filename = '5.edf'  # The 5.edf file is lacking some of the properties an edf file can have, should use some other file for testing


# The file and path are hardcoded in this file
# This should be changed later

class EdfReader:
    def __init__(self, file):
        self.file = file  # Change this to call the function instead ?

    def read_header(self):
        self.header = get_header_data(self.file)  # Move to init? google


def load_edf_file(edffile):
    if isinstance(edffile, str):
        os.chdir(r'C:\ProjectResources')
        with open(edffile, 'rb') as edf:
            return load_edf_file(edf)

    reader = EdfReader(edffile)
    reader.read_header()
    h = reader.header

    # 'b' prefix in front of string means it's a bytes literal
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


def get_header_data(f):
    h = {}
    # file = load_edf_file()

    # Here we should make sure that the file is the correct type before proceeding
    # fx. assert file.read(8) == '0       '   <-- find out if the value can be anything other than 0

    h['data_format_version'] = f.read(8).strip()
    h['local_patient_id'] = f.read(80).strip()
    h['local_recording_id'] = f.read(80).strip()

    # Fix the regex so it's in compliance to convention!
    (day, month, year) = [int(x) for x in re.findall('(\d+)', str(f.read(8)))]
    (hour, minute, sec) = [int(x) for x in re.findall('(\d+)', str(f.read(8)))]

    h['start_time'] = str(datetime.datetime(2000 + year, month, day, hour, minute, sec))
    h['bytes_in_header'] = f.read(8).strip()
    h['subtype'] = f.read(44).strip()
    # 'edf+c' => uninterrupted(contiguous) recording && 'edf+d' => interrupted recording
    h['contiguous'] = h['subtype'] != 'EDF+D'
    h['number_of_records'] = int(f.read(8))
    h['record_duration'] = float(f.read(8))
    ns = h['number_of_signals'] = int(f.read(4))  # ns variable for use when reading the data
    return h


'''
reader = EdfReader(load_edf_file())
reader.read_header()
h = reader.header

print('DataFormatVersion' + str(h['data_format_version']))
'''
