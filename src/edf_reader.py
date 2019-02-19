import os

basestring = r'C:\ProjectResources'
filename = 'test_generator_2.edf'


# The file and path are hardcoded in this file
# This should be changed later
def load_edf_file():
    os.chdir(basestring)
    with open(filename, 'rb') as edf:
        return edf.read(100)


def header():
    h = {}
    file = load_edf_file()

    # Here we should make sure that the file is the correct type before proceeding
    # fx. assert file.read(8) == '0       '   <-- find out if the value can be anything other than 0

    h['data_format_version'] = file.read(8)
    h['local_patient_id'] = file.read(80)
    h['local_recording_id'] = file.read(80)
    h['start_time__fix'] = file.read(8)
    return h


h = header()

print('DataFormatVersion' + str(h['data_format_version']))



