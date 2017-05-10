
alpha = .15
epsilon = 10 ** -6


def create_initial_pagerank_vector(graph):
    page_rank_vector = {}
    for node in graph:
        page_rank_vector[node] = 1.0 / len(graph)
    return page_rank_vector


def single_iteration_page_rank(graph, page_rank_vector, dic_weight_sum, teleporting_dic):
    next_page_rank_vector = {}
    summ = 0

    for node in graph:
        r = 0
        if len(graph[node].keys()) != 0:
            for neighbour in graph[node].keys():
                r += float((1 - alpha)) * (float(page_rank_vector[neighbour]) * float(graph[neighbour][node]['weight'])
                                           / dic_weight_sum[neighbour])

        next_page_rank_vector[node] = r
        summ += r

    leakedPR = 1 - summ

    for movie_id in teleporting_dic.keys():
        next_page_rank_vector[movie_id] += leakedPR * teleporting_dic[movie_id]

    return next_page_rank_vector


def get_distance(vector_1, vector_2):
    distance = 0
    i = 1
    while i < len(vector_1):
        distance += abs(vector_1[i] - vector_2[i])
        i += 1
    return distance


# Compute PageRank
# takes as parameters the graph, the teleporting dictionary, the dictionary of weights
def page_rank(g, teleporting_dic, dic_node_weight_sum):

    previous_page_rank_vector = create_initial_pagerank_vector(g)  # for every node set pr[node] = 1/n
    page_rank_vector = {}

    while True:

        # compute next value
        page_rank_vector = single_iteration_page_rank(g, previous_page_rank_vector
                                                      , dic_node_weight_sum, teleporting_dic)

        # evaluate the distance between the old and new pagerank vectors
        distance = get_distance(previous_page_rank_vector, page_rank_vector)

        # check convergency
        if distance <= epsilon:
            break

        previous_page_rank_vector = page_rank_vector

    return page_rank_vector
