import pprint as pp
import csv
import sys
import GraphLoader as gl
import TopicSpecificPageRank as pr

input_graph = sys.argv[1]
input_user_movie_rating_path = sys.argv[2]
input_user_id = int(sys.argv[3])


# creates a dcitionary of dictionaries
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

dic_user_movie_rating = from_file_to_dic_user_dic_movie_rating()
dic_movie_rating_for_user = dic_user_movie_rating[int(input_user_id)]
user_sum = sum(dic_movie_rating_for_user.values())

g, dic_weight_sum = gl.graph_loader(input_graph)
teleporting_dic = {}

for movie in g.nodes():

    teleporting_dic[movie] = 0
    if movie in dic_movie_rating_for_user.keys():
        teleporting_dic[movie] += float(dic_movie_rating_for_user[movie]) / user_sum

page_rank_vector = pr.page_rank(g, teleporting_dic, dic_weight_sum)


# sort and clean page rank vector
dic_movie_rating_for_user = from_file_to_dic_user_dic_movie_rating()[input_user_id]
for movie in dic_movie_rating_for_user:
    page_rank_vector.pop(movie)

final_page_rank_list = sorted(page_rank_vector.items(), key=lambda x: x[1], reverse=True)
print("****************************************************")
print("start final page rank list")
pp.pprint(final_page_rank_list)
print("end final page rank list")
print("****************************************************")
