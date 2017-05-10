import csv
import GraphLoader as gl
import TopicSpecificPageRank as pr

input_graph = "./input/movie_graph.txt"
input_movies_category = "./input/category_movies.txt"


def from_file_to_dic_topic_movies():
    f = open(input_movies_category, 'r')
    input_file_csv_reader = csv.reader(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

    dictionary = {1: [], 2: [], 3: [], 4: [], 5: []}  # since we have only five topics
    i = 1
    for movies in input_file_csv_reader:
        for movie in movies:
            dictionary.get(i).append(int(movie))
        i += 1
    f.close()
    return dictionary


g, dic_weight_sum = gl.graph_loader(input_graph)


def save_page_rank_result_into_file(result, topic_index):
    f = open('./datasets/page_rank_category_' + str(topic_index) + '.txt', 'w')
    for movie_id in result.keys():
        f.write('%s, %s\n' % (str(movie_id), str(result[movie_id])))
    f.close()

# Compute PageRank

page_rank_vector_one = {}
page_rank_vector_two = {}
page_rank_vector_three = {}
page_rank_vector_four = {}
page_rank_vector_five = {}
list_of_page_rank_vectors = [page_rank_vector_one, page_rank_vector_two, page_rank_vector_three, page_rank_vector_four,
                             page_rank_vector_five]

topic_index = 1
for page_rank_vector in list_of_page_rank_vectors:

    dic_topic_movies = from_file_to_dic_topic_movies()
    topic_movie_ids = dic_topic_movies[topic_index]


    teleporting_dic = {}

    for movie in topic_movie_ids:
        teleporting_dic[movie] = 1/float(len(topic_movie_ids))

    # compute next value
    page_rank_vector = pr.page_rank(g, teleporting_dic, dic_weight_sum)

    # save the page rank vector in a txt file
    save_page_rank_result_into_file(page_rank_vector, topic_index)

    topic_index += 1






