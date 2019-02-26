import header_reader as reader
import datetime

h1 = reader.load_edf_file('5.edf')
h2 = reader.load_edf_file('test_generator_2.edf')


# def test_number_of_elements():
# assert number of labels == number of signals

def test_data_format_version():
    assert h1['data_format_version'] == '0'
    assert h1['data_format_version'] == '0'


def test_local_patient_id():
    assert h1['local_patient_id'] == '5_MIN'
    assert h2['local_patient_id'] == 'X X X X'


def test_local_recording_id():
    assert h1['local_recording_id'] == 'Startdate 27.11.2018 Cortrium C3'
    assert h2['local_recording_id'] == 'Startdate 10-DEC-2009 X X test_generator'


def test_start_time():
    assert h1['start_time'] == str(datetime.datetime(2018, 11, 27, 9, 26, 20))
    assert h2['start_time'] == str(datetime.datetime(2009, 12, 10, 12, 44, 2))
    # (dd.mm.yy, hh.mm.ss)
    assert reader.get_start_time('11.11.12', '09.17.32') == str(datetime.datetime(2012, 11, 11, 9, 17, 32))


def test_bytes_in_header():
    assert h1['bytes_in_header'] == 2048
    assert h2['bytes_in_header'] == 3328


def test_subtype():
    assert h1['subtype'] == ''
    assert h2['subtype'] == 'EDF+C'


def test_contiguous():
    assert h1['contiguous'] is True
    assert h2['contiguous'] is True
    temp1 = 'EDF+C'
    temp2 = 'EDF+D'
    temp3 = '   some random value 123'
    assert reader.contiguity(temp1) is True
    assert reader.contiguity(temp2) is False
    assert reader.contiguity(temp3) is True


def test_number_of_records():
    assert h1['number_of_records'] == 12250
    assert h2['number_of_records'] == 600


def test_record_duration():
    assert h1['record_duration'] == 0.024
    assert h2['record_duration'] == 1.0


def test_number_of_signals():
    assert h1['number_of_signals'] == 7
    assert h2['number_of_signals'] == 12


def test_label():
    assert h1['label'] == ['ECG1', 'ECG2', 'ECG3', 'ACCX', 'ACCY', 'ACCZ', 'EVENT']
    assert h2['label'] == ['squarewave', 'ramp', 'pulse', 'ECG', 'noise', 'sine 1 Hz', 'sine 8 Hz', 'sine 8.5 Hz',
                           'sine 15 Hz', 'sine 17 Hz', 'sine 50 Hz', 'EDF Annotations']


def test_transducer_type():
    assert h1['transducer_type'] == ['Ambu electrodes', 'Ambu electrodes', 'Ambu electrodes', 'Ambu electrodes',
                                     'Ambu electrodes', 'Ambu electrodes', 'Ambu electrodes']
    assert h2['transducer_type'] == ['', '', '', '', '', '', '', '', '', '', '', '']


def test_physical_dimension():
    assert h1['physical_dimension'] == ['uV', 'uV', 'uV', 'mg', 'mg', 'mg', 'count']
    assert h2['physical_dimension'] == ['uV', 'uV', 'uV', 'uV', 'uV', 'uV', 'uV', 'uV', 'uV', 'uV', 'uV', '']


def test_physical_minimum():
    assert h1['physical_minimum'] == [-2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0]
    assert h2['physical_minimum'] == [-1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0,
                                      -1000.0, -1000.0, -1000.0, -1.0]


def test_physical_maximum():
    assert h1['physical_maximum'] == [2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0]
    assert h2['physical_maximum'] == [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0,
                                      1000.0, 1000.0, 1000.0, 1.0]


def test_digital_minimum():
    assert h1['digital_minimum'] == [-2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0, -2400.0]
    assert h2['digital_minimum'] == [-32768.0, -32768.0, -32768.0, -32768.0, -32768.0, -32768.0, -32768.0, -32768.0,
                                     -32768.0, -32768.0, -32768.0, -32768.0]


def test_digital_maximum():
    assert h1['digital_maximum'] == [2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0, 2400.0]
    assert h2['digital_maximum'] == [32767.0, 32767.0, 32767.0, 32767.0, 32767.0, 32767.0, 32767.0, 32767.0, 32767.0,
                                     32767.0, 32767.0, 32767.0]


def test_prefiltering():
    assert h1['prefiltering'] == ['', '', '', '', '', '', '']
    assert h2['prefiltering'] == ['', '', '', '', '', '', '', '', '', '', '', '']


def test_number_of_samples_per_record():
    assert h1['number_of_samples_per_record'] == [6, 6, 6, 1, 1, 1, 1]
    assert h2['number_of_samples_per_record'] == [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 51]
