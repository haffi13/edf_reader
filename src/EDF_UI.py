import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import header_reader as reader
import process_timer

from matplotlib.collections import LineCollection

pt = process_timer.Timer()

xxx = reader.load_edf_file('t.edf')
print(xxx)

fig = plt.figure("MRI_with_EEG")  # andet navn

# Load the EEG data
n_samples, n_rows = 800, 4  # her skal den hente data fra filen og selv finde antal af "Samples" og "rows"
with cbook.get_sample_data('eeg.dat') as eegfile:  # her skal den bruge vores fil
    data = np.fromfile(eegfile, dtype=float).reshape((n_samples, n_rows))
t = 10 * np.arange(n_samples) / n_samples
#tt = 10 * np.arange(0.0, 1, (n_rows / (n_rows * n_samples)))

print('len-t   -   ' + str(len(t)))
#print('len-tt   -   ' + str(len(tt)))

for i, x in enumerate(t):
    print('t' + str(i) + ' - ' + str(t[i]))
#    print('tt' + str(i) + ' - ' + str(tt[i]))

#t = np.arange(0.0, len(s) / samplerate, (len(s) / samplerate) / len(s))

print('data ..type.. - ' + str(type(data)))
print('len(data) - ' + str(len(data)))
print('str(len(data[0]))' + str(len(data[0])))

print('xxx ..type.. - ' + str(type(xxx)))
print('len(xxx) - ' + str(len(xxx)))
print('len(xxx[0]) - ' + str(len(xxx[0])))

# n_rows == num_signals
# n_samples == num_records

# Plot the EEG
ticklocs = []
ax2 = fig.add_subplot(2, 1, 2)  # det er nok ikke nødvendigt med subplottet da vi ikke har flere "plots"
ax2.set_xlim(0, 800)  # limit skal nok sættes højere da filerne kan være længere og 10 ikke vil række
ax2.set_xticks(np.arange(10))  # samme som over
dmin = data.min()
dmax = data.max()
dr = (dmax - dmin) * 0.7  # Crowd them a bit.
y0 = dmin
y1 = (n_rows - 1) * dr + dmax
ax2.set_ylim(y0, y1)

segs = []
indx = 0
for i in range(n_rows):
    print(indx)
    #print('t - ' + str(t))
    print('len -> t - ' + str(len(t)))
    #print('data[:, i] - ' + str(data[:, i]))
    print('len -> data[:, i] - ' + str(len(data[:, i])))
    #segs.append(np.column_stack((t, data[:, i])))
    segs.append(np.column_stack((t, xxx[i, :])))
    ticklocs.append(i * dr)
    indx += 1

offsets = np.zeros((n_rows, 2), dtype=float)
offsets[:, 1] = ticklocs

lines = LineCollection(segs, offsets=offsets, transOffset=None)
ax2.add_collection(lines)

# Set the yticks to use axes coordinates on the y axis
ax2.set_yticks(ticklocs)
ax2.set_yticklabels(['PG3', 'PG5', 'PG7', 'PG9'])  # her skal den hente labels fra EDF fil

ax2.set_xlabel('Time (s)')


plt.tight_layout()
plt.show()