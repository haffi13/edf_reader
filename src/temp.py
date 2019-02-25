# This file is not supposed to be in the project. It's here temporarily so we can test components seperately
# before integrating them with the rest of the code.

import edf_reader as e
import numpy as np

EVENT_CHANNEL = 'EDF Annotations'

h = e.load_edf_file('5.edf')


def convert_record(self, raw_record):
    '''Convert a raw record to a (time, signals, events) tuple based on
    information in the header.
    '''
    h = self.header
    dig_min, phys_min, gain = self.dig_min, self.phys_min, self.gain
    time = float('nan')
    signals = []
    events = []
    for (i, samples) in enumerate(raw_record):
        if h['label'][i] == EVENT_CHANNEL:
            ann = tal(samples)
            time = ann[0][0]
            events.extend(ann[1:])
        else:
            # 2-byte little-endian integers
            dig = np.fromstring(samples, '<i2').astype(np.float32)
            phys = (dig - dig_min[i]) * gain[i] + phys_min[i]
            signals.append(phys)

    return time, signals, events


def tal(tal_str):
    '''Return a list with (onset, duration, annotation) tuples for an EDF+ TAL
  stream.
  '''
    exp = '(?P<onset>[+\-]\d+(?:\.\d*)?)' + \
          '(?:\x15(?P<duration>\d+(?:\.\d*)?))?' + \
          '(\x14(?P<annotation>[^\x00]*))?' + \
          '(?:\x14\x00)'

    def annotation_to_list(annotation):
        return unicode(annotation, 'utf-8').split('\x14') if annotation else []

    def parse(dic):
        return (
            float(dic['onset']),
            float(dic['duration']) if dic['duration'] else 0.,
            annotation_to_list(dic['annotation']))

    return [parse(m.groupdict()) for m in re.finditer(exp, tal_str)]


'''
nsamp = np.unique(
    [n for l, n in zip(h['label'], h['number_of_samples_per_record'])
     if l != EVENT_CHANNEL])
# assert nsamp.size == 1, 'Multiple sample rates not supported!'
sample_rate = float(nsamp[0]) / h['record_duration']

print(nsamp.size)
print(nsamp)
'''

# number, for
