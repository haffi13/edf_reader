import header_reader

#  h = header_reader.load_edf_file('5.edf')


class RecordReader:
    def __init__(self):
        self.header = header_reader.load_edf_file('5.edf')
        self.dig_min, self.phys_min, self.phys_range, self.dig_range, self.gain = read_header(self.header)
        print('dig range  -  ' + str(self.dig_range))

#    def read_raw_record(self):
#        result = []
#        for num_samples in self.header['number_of_samples_per_record']:




# def get_raw_record_reading(header)


def read_header(header):
    dmin = header['digital_minimum']
    pmin = header['physical_minimum']
    pran = header['physical_range']
    dran = header['digital_range']
    return dmin, pmin, pran, dran, (pran / dran)


def get_record_data():  # main method
    #reader = RecordReader
    reader = header_reader.load_edf_file('5.edf')
    print(reader)



def get_range(max, min):
    return max - min

'''
    h['data_format_version'] = f.read(8).decode('ascii').strip()
    h['local_patient_id'] = f.read(80).decode('ascii').strip()
    h['local_recording_id'] = f.read(80).decode('ascii').strip()
    h['start_time'] = get_start_time(f.read(8).decode('ascii'), f.read(8).decode('ascii'))
    h['bytes_in_header'] = int(f.read(8))
    h['subtype'] = f.read(44).decode('ascii').strip()
    h['contiguous'] = contiguity(h['subtype'])
    h['number_of_records'] = int(f.read(8))
    h['record_duration'] = float(f.read(8))
    ns = h['number_of_signals'] = int(f.read(4))  # ns variable for use when reading the data

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
'''