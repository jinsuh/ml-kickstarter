import argparse
import cPickle
import datetime
import numpy as np
import math
import operator

def load_binary(file_name):
    with open(file_name, 'rb') as f:
        return cPickle.load(f)

def load_data():
    print 'Loading projects...'
    projects = np.load('projects.npy')
    print 'Loading statuses...'
    statuses = load_binary('statuses.pkl')
    print 'Loading tweets...'
    tweets = np.load('tweets.npy')
    print 'Loading graph...'
    graph = np.load('graph.pkl')

    # conver to numpy arrays if needed
    statuses = np.array(statuses)

    return projects, statuses, tweets, graph

def squared_distance(data_first, data_second):
	distance = math.pow((data_first - data_second), 2)
	# for i in xrange(1000):
	# 	distance += math.pow((data_first[i][2]- data_second[i][2]), 2)
	# 	distance += math.pow((data_first[i][3]- data_second[i][3]), 2)
	return distance

def dist_from_data(training_set, testing_inst):
	distances = []
	for i in xrange(len(training_set)):
		dist = 0
		#projects data
		data_first = training_set[i]['projects'][1]
		data_second = testing_inst['projects'][1]
		dist += squared_distance(data_first, data_second)
		data_first = training_set[i]['projects'][3]
		data_second = testing_inst['projects'][3]
		dist += squared_distance(data_first, data_second)
		data_first = training_set[i]['projects'][4]
		data_second = testing_inst['projects'][4]
		dist += squared_distance(data_first, data_second)

		#statuses data
		status_length = len(training_set[i]['statuses'])
		for j in xrange(status_length):
			data_first = training_set[i]['statuses'][j][1]
			data_second = testing_inst['statuses'][j][1]
			dist += squared_distance(data_first, data_second)
			data_first = training_set[i]['statuses'][j][2]
			data_second = testing_inst['statuses'][j][2]
			dist += squared_distance(data_first, data_second)

		#twitter data
		# tweet_length = len(training_set[i]['tweets'])
		# for j in xrange(status_length):
		# 	data_first = training_set[i]['tweets'][j][0]
		# 	data_second = testing_inst['tweets'][j][0]
		# 	dist += squared_distance(data_first, data_second)
		# 	data_first = training_set[i]['tweets'][j][1]
		# 	data_second = testing_inst['tweets'][j][1]
		# 	dist += squared_distance(data_first, data_second)
		# 	data_first = training_set[i]['tweets'][j][2]
		# 	data_second = testing_inst['tweets'][j][2]
		# 	dist += squared_distance(data_first, data_second)
		# 	data_first = training_set[i]['tweets'][j][3]
		# 	data_second = testing_inst['tweets'][j][3]
		# 	dist += squared_distance(data_first, data_second)
		# 	data_first = training_set[i]['tweets'][j][4]
		# 	data_second = testing_inst['tweets'][j][4]
		# 	dist += squared_distance(data_first, data_second)
		dist = math.sqrt(dist)
		distances.append((training_set[i], dist))
	return distances

def knn(training_set, testing_inst, k):
	distances = dist_from_data(training_set, testing_inst)
	distances.sort(key = operator.itemgetter(1))
	neighbors = []
	for i in xrange(k):
		neighbors.append(distances[i][0])
	return neighbors

def predict(neighbors):
	counter = [0, 0]
	for i in xrange(len(neighbors)):
		index = neighbors[i]['projects'][2]
		counter[index] += 1
	return counter[1] > counter[0]

def sort_data(projects, statuses, tweets, graph, index_start, index_end):
	print "Sorting data"
	length = len(projects)
	training_set = []
	testing_set = []
	for i in xrange(length):
		d = dict()
		d['projects'] = projects[i]
		d['statuses'] = statuses[i]
		d['tweets'] = tweets[i]
		if (i < index_start or i > index_end):
			training_set.append(d)
		else:
			testing_set.append(d)
	return training_set, testing_set

#10-cross-fold validation
def run():
	projects, statuses, tweets, graph = load_data()
	accuracy_mean_sum = 0
	length = len(projects)
	accuracy_tracker = []
	for i in xrange(10):
		index_start = (length / 10) * i
		index_end = (length / 10) * (i + 1)
		if (index_end > length - 1):
			print "cutfoff correction"
			index_end = length - 1
		training_set, testing_set = sort_data(projects, statuses, tweets, graph, index_start, index_end)
		accuracy_total = 0
		count_within = 0
		for test_data in testing_set:
			neighbors = knn(training_set, test_data, 25)
			prediction = predict(neighbors)
			if (prediction == test_data['projects'][2]):
				accuracy_total += 1
			count_within += 1
			print "inside", accuracy_total / float(count_within)
			if i == 0:
				accuracy_tracker.append(accuracy_total / float(count_within))
				cPickle.dump(accuracy_tracker, open("track.p", "wb"))
		accuracy_mean_sum = (accuracy_mean_sum * i) + (accuracy_total / float(len(testing_set)))
		print "one crossfold", accuracy_mean_sum / float(i + 1)
	accuracy_mean = accuracy_mean_sum / float(10)
	print accuracy_mean

if __name__ == '__main__':
    
	accuracy_mean = run()
	print accuracy_mean