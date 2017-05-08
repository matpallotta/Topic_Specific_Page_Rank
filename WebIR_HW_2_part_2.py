import pprint as pp
import csv
import networkx as nx
import time
import sys

# input_graph = sys.argv[1]
# input_user_movie_rating_path = sys.argv[2]
# input_user_id = int(sys.argv[3])

input_graph = "./datasets/movie_graph.txt"
input_user_movie_rating_path = "./datasets/user_movie_rating.txt"
input_user_id = 2290


alpha = .15
epsilon = 10**-6


def from_file_to_dic_user_dic_movie_rating():
    dictionary = {}
    input_file = open(input_user_movie_rating_path, 'r')
    input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
    for user_movie_rating in input_file_csv_reader:
        if int(user_movie_rating[0]) not in dictionary:
            dictionary[int(user_movie_rating[0])] = {int(user_movie_rating[1]): int(user_movie_rating[2])}
        else:
            dictionary[int(user_movie_rating[0])][int(user_movie_rating[1])] = int(user_movie_rating[2])
    input_file.close()
    return dictionary

def get_distance(vector_1, vector_2):
    distance = 0
    i = 1
    while i < len(vector_1):
        distance += abs(vector_1[i] - vector_2[i])
        i += 1
    return distance


def create_initial_pagerank_vector(graph):
    page_rank_vector = {}
    for node in graph:
        page_rank_vector[node] = 1.0/len(graph)
    return page_rank_vector


def single_iteration_page_rank(graph, page_rank_vector_dic, alpha, dic_weight_sum):
    next_page_rank_vector = {}
    summ = 0

    for node in graph:
        r = 0
        if len(graph[node].keys()) != 0:
            for neighbour in graph[node]:
                r += float((1 - alpha)) * (float(page_rank_vector_dic[neighbour]) * float(graph[neighbour][node]['weight'])
                                           / dic_weight_sum[neighbour])

        next_page_rank_vector[node] = r
        summ += r

    leakedPR = 1 - summ
    dic_user_movie_rating = from_file_to_dic_user_dic_movie_rating()
    dic_movie_rating_for_user = dic_user_movie_rating[int(input_user_id)]
    for movie, rating in dic_movie_rating_for_user.items():
        next_page_rank_vector[int(movie)] += float(leakedPR) * float(rating)/sum(dic_movie_rating_for_user.values())

    return next_page_rank_vector



# undirected graph creation
g = nx.Graph()


# load graph
input_file = open(input_graph, 'r')
input_file_csv_reader = csv.reader(input_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

dic_node_weight_sum = {}

for node_node_weight in input_file_csv_reader:
    g.add_node(int(node_node_weight[0]))
    g.add_node(int(node_node_weight[1]))

    g.add_edge(int(node_node_weight[0]), int(node_node_weight[1]), weight=int(node_node_weight[2]))

    if int(node_node_weight[0]) not in dic_node_weight_sum:
        dic_node_weight_sum[int(node_node_weight[0])] = 0

    if int(node_node_weight[1]) not in dic_node_weight_sum:
        dic_node_weight_sum[int(node_node_weight[1])] = 0

    dic_node_weight_sum[int(node_node_weight[0])] += int(node_node_weight[2])
    dic_node_weight_sum[int(node_node_weight[1])] += int(node_node_weight[2])

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
'''
print("start of print of initial page rank vector")
print(previous_page_rank_vector)
print("end of print of initial page rank vector")
'''
page_rank_vector = {}
num_iterations = 0  # t=0
total_start_time = time.clock()
while True:
    start_time = time.clock()
    # pp.pprint(previous_page_rank_vector)
    # print ("END previous_PR_vector")

    # compute next value
    page_rank_vector = single_iteration_page_rank(g, previous_page_rank_vector, alpha, dic_node_weight_sum)

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
    pp.pprint (page_rank_vector)

    page_rank_vector_sum = sum(page_rank_vector.values())
    print(" page rank vector sum: " + str(page_rank_vector_sum))
    print("time this iteration took: " + str((end_time - start_time)) + "sec")
    print("total time : " + str((end_time - total_start_time)) + "sec")


dic_movie_rating_for_user = from_file_to_dic_user_dic_movie_rating()[input_user_id]
for movie in dic_movie_rating_for_user.keys():
    page_rank_vector.pop(movie)

final_page_rank_list = sorted(page_rank_vector.items(), key=lambda x: x[1], reverse=True)
print ("****************************************************")
print("start final page rank list")
pp.pprint(final_page_rank_list)
print("end final page rank list")
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


