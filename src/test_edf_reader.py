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

h1 = reader.load_edf_file('5.edf')
h2 = reader.load_edf_file('test_generator_2.edf')


def test_data_format_version():
    assert str(h1['data_format_version']) == '0'


def test_local_patient_id():
    assert str(h1['local_patient_id']) == '5_MIN'


def test_local_recording_id():
    assert str(h1['local_recording_id']) == 'Startdate 27.11.2018 Cortrium C3'


def test_start_time():
    assert h1['start_time'] == str(datetime.datetime(2018, 11, 27, 9, 26, 20))


def test_bytes_in_header():
    assert h['bytes_in_header'] == '2048'


def test_subtype():
    assert str(h['subtype']) == ''


def test_contiguous():
    assert h['contiguous'] == True


def test_number_of_records():
    assert h1['number_of_records'] == 12250


def test_record_duration():
    assert h1['record_duration'] == 0.024


def test_number_of_signals():
    assert h1['number_of_signals'] == 7


