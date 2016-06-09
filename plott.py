import argparse
import cPickle
import datetime
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

def plot_status():
	status = cPickle.load(open("status_1.p", "rb"))
	real_status = []
	x_axis = []
	count = 0
	for i in xrange(100):
		real_status.append(status[count])
		x_axis.append(count)
		count += 10
	plt.plot(x_axis, real_status)
	plt.xlabel("Number of Timestamp Samples Used")
	plt.ylabel("Accuracy Average")
	plt.title("Average Accuracy Over the Number of Timestamp Samples")
	plt.show()

def plot_tracker():
	tracker = (cPickle.load(open("track.p", "rb")))
	print len(tracker)
	plt.plot(tracker)
	plt.xlabel("Test Sample")
	plt.ylabel("Accuracy Average")
	plt.title("Average Accuracy Over the Number of Test Samples")
	plt.show()

def run():
	# plot_tracker()
	plot_status()

if __name__ == '__main__':
	run()