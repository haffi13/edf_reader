import matplotlib.pyplot as plt
import random
from matplotlib import style
import csv
import matplotlib.cbook as cbook
import matplotlib.cm as cm
import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.ticker import MultipleLocator

n_samples, n_rows = 800, 4



#style.use('dark_background')
#style.use('fivethirtyeight')

x = []
y = []

with open('testmatplotlib.txt', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

plt.plot(x,y, label='test')
plt.grid(True)

plt.show()


#dette er hvad der skal kigges på

fig = plt.figure("MRI_with_EEG")  # andet navn

# Load the EEG data
n_samples, n_rows = 800, 4  # her skal den hente data fra filen og selv finde antal af "Samples" og "rows"
with cbook.get_sample_data('eeg.dat') as eegfile:  # her skal den bruge vores fil
    data = np.fromfile(eegfile, dtype=float).reshape((n_samples, n_rows))
t = 10 * np.arange(n_samples) / n_samples

# Plot the EEG
ticklocs = []
ax2 = fig.add_subplot(2, 1, 2)  # det er nok ikke nødvendigt med subplottet da vi ikke har flere "plots"
ax2.set_xlim(0, 10)  # limit skal nok sættes højere da filerne kan være længere og 10 ikke vil række
ax2.set_xticks(np.arange(10))  # samme som over
dmin = data.min()
dmax = data.max()
dr = (dmax - dmin) * 0.7  # Crowd them a bit.
y0 = dmin
y1 = (n_rows - 1) * dr + dmax
ax2.set_ylim(y0, y1)

segs = []
for i in range(n_rows):
    segs.append(np.column_stack((t, data[:, i])))
    ticklocs.append(i * dr)

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















#fig = plt.figure()



# def create_plots():
#     xs = []
#     ys = []
#
#     for i in range(20):
#         x = i
#         y = random.randrange(10)
#
#         xs.append(x)
#         ys.append(y)
#     return xs, ys


#ax1 = plt.subplot2grid((20,1),(0,0), rowspan=2, colspan=1)
#plt.grid(True)
#ax1.axes.get_yaxis().set_visible(False)


# ax2 = plt.subplot2grid((20,1),(0,0), rowspan=15, colspan=1, )
# plt.grid(True)
# #ax2.axes.get_yaxis().set_visible(False)
# ax2v=ax2.twinx()
# ax3v=ax2.twinx()
# ax4v=ax2.twinx()
# ax5v=ax2.twinx()

# ax3 = plt.subplot2grid((20,1),(4,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax3.axes.get_yaxis().set_visible(False)
#
#
# #ax3 =fig.add_axes([0.0, 0.4, 0.50, 0.20])
#
# ax4 = plt.subplot2grid((20,1),(6,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax4.axes.get_yaxis().set_visible(False)
#
# ax5 = plt.subplot2grid((20,1),(8,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax5.axes.get_yaxis().set_visible(False)
#
# ax6 = plt.subplot2grid((20,1),(10,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax6.axes.get_yaxis().set_visible(False)
#
# ax7 = plt.subplot2grid((20,1),(12,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax7.axes.get_yaxis().set_visible(False)
#
# ax8 = plt.subplot2grid((20,1),(14,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax8.axes.get_yaxis().set_visible(False)
#
# ax9 = plt.subplot2grid((20,1),(16,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax9.axes.get_yaxis().set_visible(False)
#
# ax10 = plt.subplot2grid((20,1),(18,0), rowspan=2, colspan=1, sharex=ax1, sharey=ax1)
# plt.grid(True)
# ax10.axes.get_yaxis().set_visible(False)

#ax1 = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)


#x,y = create_plots()
#ax1.plot(x,y, label='aaa', linewidth=1)
#
#
# x,y = create_plots()
# ax2.plot(x,y, color='y', linewidth=1, label='ax2')
# ax2.annotate('test', xy=(0,5))
#
#
#
# x,y = create_plots()
# ax2v.plot(x,y, linewidth=1)
# ax2v.set_ylim(10, -1)
#ax2v.get_ylim
#ax2v.set_ylim()

# x,y = create_plots()
# ax3v.plot(x,y, color='r', linewidth=1)
#
# x,y = create_plots()
# ax4v.plot(x,y, color='g', linewidth=1)
#
# x,y = create_plots()
# ax5v.plot(x,y, color='pink', linewidth=1)

#x,y = create_plots()
#ax3.plot(x,y, linewidth=1)

# x,y = create_plots()
# ax4.plot(x,y, linewidth=1)
#
# x,y = create_plots()
# ax5.plot(x,y, linewidth=1)
#
# x,y = create_plots()
# ax6.plot(x,y, linewidth=1)
#
# x,y = create_plots()
# ax7.plot(x,y, linewidth=1)
#
# x,y = create_plots()
# ax8.plot(x,y, linewidth=1)
#
# x,y = create_plots()
# ax9.plot(x,y, linewidth=1)
#
# x,y = create_plots()
# ax10.plot(x,y, linewidth=1)

#plt.subplots_adjust(left=0.00, right=1, top=1, bottom=0.00, hspace=0.0)

#plt.show()

#fig = plt.figure()
#ax1 = plt.subplot2grid((1, 1), (0, 0))

#x, y = np.random.rand(2, 20)
#x1, y1 = np.random.rand(2, 20)
#x2, y2 = np.random.rand(2, 20)
#x3, y3 = np.random.rand(2, 20)


#ax1.plot(x, y, label='test', color='b')
#ax1.plot(x1, y1, label='test1', color='r')
#plt.plot(x2, y2, label='test2', color='g')
#plt.plot(x3, y3, label='test3', color='y')

#plt.xlabel('x')
#plt.ylabel('y')
#plt.title('test title')
#plt.show()
