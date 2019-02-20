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
''' Done by Jonas '''
def test_bytes_in_header():
    assert h['bytes_in_header'] == '2048'

def test_subtype():
    assert str(h['subtype']) == ''

def test_contiguous():
    assert h['subtype'] == True

''' '''


def test_number_of_records():
def test_record_duration():
def test_number_of_signals():


