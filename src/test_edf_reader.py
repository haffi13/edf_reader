import edf_reader as reader
import datetime

'''
    h['data_format_version'] 
    h['local_patient_id'] 
    h['local_recording_id'] 
    h['start_time'] 
    h['bytes_in_header'] 
    h['subtype'] 
    h['contiguous'] 	x2
    h['number_of_records'] 
    h['record_duration'] 
    h['number_of_signals'] 
'''

h = reader.load_edf_file('5.edf')

def test_data_format_version():


def test_local_patient_id():



def test_local_recording_id():


def test_start_time():
    h = reader.load_edf_file('5.edf')
    b = isinstance(h, dict)
    assert b == True

def test_bytes_in_header():
def test_subtype():
def test_contiguous():
def test_number_of_records():
def test_number_of_signals():
