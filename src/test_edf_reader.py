import edf_reader as reader
import datetime

h1 = reader.load_edf_file('5.edf')
h2 = reader.load_edf_file('test_generator_2.edf')


def test_data_format_version():
    assert h1['data_format_version'] == '0'


def test_local_patient_id():
    assert h1['local_patient_id'] == '5_MIN'


def test_local_recording_id():
    assert h1['local_recording_id'] == 'Startdate 27.11.2018 Cortrium C3'


def test_start_time():
    assert h1['start_time'] == str(datetime.datetime(2018, 11, 27, 9, 26, 20))


def test_bytes_in_header():
    assert h1['bytes_in_header'] == 2048


def test_subtype():
    assert h1['subtype'] == ''


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


'''
 All tests above are valid as is
'''


def test_label():
    assert h1['label'] == ['ECG1', 'ECG2', 'ECG3', 'ACCX', 'ACCY', 'ACCZ', 'EVENT']


def test_transducer_type():
    assert h1['transducer_type'] == ['Ambu electrodes', 'Ambu electrodes', 'Ambu electrodes', 'Ambu electrodes',
                                     'Ambu electrodes', 'Ambu electrodes', 'Ambu electrodes']


def test_physical_dimension():
    assert h1['physical_dimension'] == ['uV', 'uV', 'uV', 'mg', 'mg', 'mg', 'count']


def test_physical_minimum():
    assert h1['physical_minimum'] == [-2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0]


def test_physical_maximum():
    assert h1['physical_maximum'] == [2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0]


def test_digital_minimum():
    assert h1['digital_minimum'] == [-2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0]


def test_digital_maximum():
    assert h1['digital_maximum'] == [2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0]


def test_prefiltering():
    assert h1['prefiltering'] == ['', '', '', '', '', '', '']


def test_number_of_samples_per_record():
    assert h1['number_of_samples_per_record'] == [6, 6, 6, 1, 1, 1, 1]
