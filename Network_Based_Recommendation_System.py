import csv
import pprint as pp
import networkx as nx
import time


input_graph = './datasets/movie_graph.txt'


alpha = .15
epsilon = 10**-6
topic_movie_ids = [1, 2, 3, 4, 5]  # a set of movies that create the topic


# Complete the method, please.
def create_initial_pagerank_vector(graph):
	page_rank_vector = {}
	for node in graph:
		page_rank_vector[node] = 1.0/len(graph)
	return page_rank_vector


# Complete the method, please.
def single_iteration_page_rank(graph, page_rank_vector, alpha):
	next_page_rank_vector = {}
	summ = 0

	for node in graph:
		r = 0
		if len(graph[node].keys()) != 0:
			for neighbour in graph[node].keys():
				r += float((1-alpha)) * (float(page_rank_vector[neighbour]) * float(graph[neighbour][node]['weight'])
										 /float(weight_sum_edges(graph, neighbour)))

		next_page_rank_vector[node] = r
		summ += r

	leakedPR = 1 - summ

	for movie_id in topic_movie_ids:
			next_page_rank_vector[movie_id] += leakedPR/len(topic_movie_ids)

	return next_page_rank_vector


def weight_sum_edges(graph, node):
	weight_sum = 0

	for neighbour, attrs in graph[node].items():
		weight_sum += attrs['weight']
	return weight_sum


def get_distance(vector_1, vector_2):
	distance = 0
	i = 1
	while i < len(vector_1):
		distance += abs(vector_1[i] - vector_2[i])
		i += 1
	return distance


# undirected graph creation
g = nx.Graph()


# load graph
input_file = open(input_graph, 'r')
input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
for node_node_weight in input_file_csv_reader:
	g.add_node(int(node_node_weight[0]))
	g.add_node(int(node_node_weight[1]))
	g.add_edge(int(node_node_weight[0]), int(node_node_weight[1]), weight=int(node_node_weight[2]))
input_file.close()

'''
# print graph
print
i = 0
for node in g:
	print(str(node) + " -- " + str(g[node]))
	i += 1
	print (i)
print
'''


# reverse_g = g.reverse(copy=True)

'''
# print reverse graph
print
for node in reverse_g:
	print(str(node) + " -- " + str(reverse_g[node]))
print
'''


# Compute PageRank
previous_page_rank_vector = create_initial_pagerank_vector(g)  # for every node set pr[node] = 1/n
print(previous_page_rank_vector)
page_rank_vector = {}
num_iterations = 0  # t=0
while True:
	start_time = time.clock()
	# pp.pprint(previous_page_rank_vector)
	# print ("END previous_PR_vector")

	# compute next value
	page_rank_vector = single_iteration_page_rank(g, previous_page_rank_vector, alpha)

	end_time = time.clock()

	num_iterations += 1

	# print (page_rank_vector)

	# print (previous_page_rank_vector)
	# evaluate the distance between the old and new pagerank vectors
	distance = get_distance(previous_page_rank_vector, page_rank_vector)

	print
	print(" iteration number " + str(num_iterations))
	print(" distance= " + str(distance))
	# check convergency
	if distance <= epsilon:
		print
		print(" Convergence!")
		print
		break

	previous_page_rank_vector = page_rank_vector
	print (page_rank_vector)

	page_rank_vector_sum = sum(page_rank_vector.values())
	print(" page rank vector sum: " + str(page_rank_vector_sum))
	print ("time this iteration took: " + str(end_time - start_time)/60 + "mins")
	print ("****************************************************")

# Useful for debugging ;)
'''
print "start PR"
pr = nx.pagerank(g, alpha=dumping_factor)
print "end PR"
print
pp.pprint(pr)
print
'''































