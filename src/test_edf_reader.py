import edf_reader as reader
import datetime

h1 = reader.load_edf_file('5.edf')
h2 = reader.load_edf_file('test_generator_2.edf')


def test_data_format_version():
    assert h1['data_format_version'] == '0'


def test_local_patient_id():
    assert h1['local_patient_id'] == b'5_MIN'


def test_local_recording_id():
    assert h1['local_recording_id'] == b'Startdate 27.11.2018 Cortrium C3'


def test_start_time():
    assert h1['start_time'] == str(datetime.datetime(2018, 11, 27, 9, 26, 20))



def test_bytes_in_header():
    assert int(h1['bytes_in_header']) == 2048


def test_subtype():
    assert h1['subtype'] == b''


def test_contiguous():
    assert h1['contiguous'] is True
    temp1 = 'EDF+C'
    temp2 = 'EDF+D'
    temp3 = '   some random value 123'
    assert reader.contiguity(temp1) is True
    assert reader.contiguity(temp2) is False
    assert reader.contiguity(temp3) is True


def test_number_of_records():
    assert h1['number_of_records'] == 12250


def test_record_duration():
    assert h1['record_duration'] == 0.024


def test_number_of_signals():
    assert h1['number_of_signals'] == 7
