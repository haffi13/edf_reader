import edf_reader as reader
import datetime






def test_start_time():
    h = reader.load_edf_file('5.edf')
    b = isinstance(h, dict)
    assert b == True
