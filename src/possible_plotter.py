import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import header_reader as reader
import process_timer
import math
from matplotlib.widgets import Slider

from matplotlib.collections import LineCollection

pt = process_timer.Timer()

xxx, samplerate = reader.load_edf_file('t.edf')
print(xxx)

fig = plt.figure("MRI_with_EEG")  # andet navn

# Load the EEG data
# n_samples, n_rows = 800, 4  # her skal den hente data fra filen og selv finde antal af "Samples" og "rows"
# with cbook.get_sample_data('eeg.dat') as eegfile:  # her skal den bruge vores fil
#    data = np.fromfile(eegfile, dtype=float).reshape((n_samples, n_rows))
# t = 10 * np.arange(n_samples) / n_samples

# t = len(xxx[0]) * np.arange(len(xxx[0])) / len(xxx[0]) -> potential, needs fix
# t = np.arange(0.0, len(xxx[0]), (len(xxx[0]/samplerate) / ((len(xxx[0] / samplerate) * len(xxx)))))
# t = np.arange(0.0, len(s) / samplerate, (len(s) / samplerate) / len(s))
t = len(xxx[0]) / samplerate * np.arange(len(xxx[0])) / len(xxx[0])

print('xxx ..type.. - ' + str(type(xxx)))
print('len(xxx) - ' + str(len(xxx)))
print('len(xxx[0]) - ' + str(len(xxx[0])))
print('len(t) - ' + str(len(t)))
print('samplerate - ' + str(samplerate))

# prss = (len(xxx[0]) / samplerate) / len(xxx[0])
# print('prss - ' + str(prss))
# xls = np.arange(0.0, xxx[0] / samplerate, (xxx[0] / samplerate) / xxx[0])
# print(xls)
ddd = (np.arange(0.0, (len(xxx[0]) / samplerate), (len(xxx[0]) / samplerate) / len(xxx[0])))

print('type(ddd) - ' + str(type(ddd)))
# ddd = ddd.tolist()
print('type(ddd) - ' + str(type(ddd)))
lll = np.arange(0.0, (len(xxx[0]) / samplerate), 1)
lll = lll.tolist()

print('ddd len - ' + str(len(ddd)))
print('lll len - ' + str(len(lll)))
print('type(ddd) - ' + str(type(ddd)))
print('type(lll) - ' + str(type(lll)))

# Plot the EEG
ticklocs = []
print('ticklocs done')
ax2 = plt.subplot2grid((10, 1), (0, 0),
                       rowspan=10)  # det er nok ikke nødvendigt med subplottet da vi ikke har flere "plots"
print('subplot2grid done')
ax2.set_xlim(0,
             len(xxx[0]) / samplerate)  # limit skal nok sættes højere da filerne kan være længere og 10 ikke vil række
print('set_xlim done')
# ax2.set_xticks(ddd)  # samme som over
# ax2.set_xticks(ddd, minor=False)
ax2.set_xticks(lll)
print('set_xticks done')
dmin = math.floor(xxx.min())
dmax = math.ceil(xxx.max())
dr = (dmax - dmin) * 0.7  # Crowd them a bit.   <------------member!!
y0 = dmin
y1 = (len(xxx) - 1) * dr + dmax
ax2.set_ylim(y0, y1)
print('set_ylim done')
print('dmin - ' + str(dmin))
print('dmax - ' + str(dmax))

segs = []
print('lenxxx0 / samprate - ' + str(len(xxx[0]) / samplerate))
for i in range(len(xxx)):
    print('i - ' + str(i))
    segs.append(np.column_stack((t, xxx[i, :])))
    ticklocs.append(i * dr)

offsets = np.zeros((len(xxx), 2), dtype=float)
offsets[:, 1] = ticklocs

print(ticklocs)
print(type(ticklocs))

lines = LineCollection(segs, offsets=offsets, transOffset=None)
ax2.add_collection(lines)

# Set the yticks to use axes coordinates on the y axis
# ax2.set_yticks(ticklocs)
# ax2.set_yticklabels(['PG3', 'PG5', 'PG7', 'PG9'])  # her skal den hente labels fra EDF fil

plt.axis([0, 10, y0, y1])  # first 2 numbers are range that is visible at a time, last 2 are min/max for y axis
axpos = plt.axes([0.2, 0.1, 0.65, 0.03])  # position of the slider bar
spos = Slider(axpos, 'Pos', 0.1, 590)  # position, label, step size, length(max - visible range at a time)

ax2.set_xlabel('Time (s)')

# plt.tight_layout()
plt.show()
