import pyedflib
import numpy as np
import os
import process_timer
import pandas as pd
import matplotlib.pyplot as plt, mpld3

pt = process_timer.Timer()

os.chdir(r'C:\ProjectResources')

class EdfData():
	def __init__(self, file_name):
		self.file = pyedflib.EdfReader(file_name)

	def get_data(self):
		pt.start()
		self.number_of_signals = self.file.signals_in_file
		self.duration = self.file.file_duration
		self.starttime = self.file.getStartdatetime() # returns in format: 2019-01-20 03:28:03
		self.number_of_records = self.file.datarecords_in_file
		self.number_of_annotations = self.file.annotations_in_file
		self.labels = self.file.getSignalLabels()
		self.annotations = self.file.readAnnotations()
		self.recording_additional = self.file.getRecordingAdditional()

		# Setting fixed array sizes in accordance with the file format.
		self.labels = np.chararray(self.number_of_signals, 16, True)
		self.phys_dimensions = np.chararray(self.number_of_signals, 8, True)
		self.phys_max = self.phys_min = self.dig_max = self.dig_min = np.empty(self.number_of_signals)
		self.transducers = self.prefilters = np.chararray(self.number_of_signals, 80, True)
		self.sample_frequencies = self.file.getSampleFrequencies()

		self.signals = []

		for channel in np.arange(self.number_of_signals):  # change to self.number_of_signals.............
			self.labels[channel] = self.file.getLabel(channel)
			self.phys_min[channel] = self.file.getPhysicalMinimum(channel)
			self.phys_max[channel] = self.file.getPhysicalMaximum(channel)
			self.phys_dimensions[channel] = self.file.getPhysicalDimension(channel)
			self.dig_min[channel] = self.file.getDigitalMinimum(channel)
			self.dig_max[channel] = self.file.getDigitalMaximum(channel)
			self.prefilters[channel] = self.file.getPrefilter(channel)
			self.transducers[channel] = self.file.getTransducer(channel)
			self.signals.append(self.file.readSignal(channel))






# Call update line from here. Use the params of udate line to get the x range it should be getting data from.
def update(val):
    pos = spos.val
    ax2.axis([pos,pos + 10, y0, y1])
    fig.canvas.draw_idle()



# h1 is the name of the plot
def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw()

