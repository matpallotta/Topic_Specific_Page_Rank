import sys
import csv
import pprint as pp

# user_preference_vector = sys.argv[1]
user_preference_vector = "3_4_0_2_1"


def from_file_to_dic_page_rank(file_path):
    dictionary = {}
    input_file = open(file_path, 'r')
    input_file_csv_reader = csv.reader(input_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    for movie_pr in input_file_csv_reader:
        dictionary[int(movie_pr[0])] = float(movie_pr[1])
    input_file.close()
    return dictionary

dic_movie_page_rank_one = from_file_to_dic_page_rank('./datasets/page_rank_category_1.txt')
dic_movie_page_rank_two = from_file_to_dic_page_rank('./datasets/page_rank_category_2.txt')
dic_movie_page_rank_three = from_file_to_dic_page_rank('./datasets/page_rank_category_3.txt')
dic_movie_page_rank_four = from_file_to_dic_page_rank('./datasets/page_rank_category_4.txt')
dic_movie_page_rank_five = from_file_to_dic_page_rank('./datasets/page_rank_category_5.txt')

dic_recomendations = {}

for movie_id in dic_movie_page_rank_one.keys():
    dic_recomendations[movie_id] = 0
    dic_recomendations[movie_id] += int(user_preference_vector[0]) * dic_movie_page_rank_one[movie_id]
    dic_recomendations[movie_id] += int(user_preference_vector[2]) * dic_movie_page_rank_two[movie_id]
    dic_recomendations[movie_id] += int(user_preference_vector[4]) * dic_movie_page_rank_three[movie_id]
    dic_recomendations[movie_id] += int(user_preference_vector[6]) * dic_movie_page_rank_four[movie_id]
    dic_recomendations[movie_id] += int(user_preference_vector[8]) * dic_movie_page_rank_five[movie_id]

sorted_final_movie_pr_rec = sorted(dic_recomendations.items(), key=lambda x: x[1], reverse=True)
pp.pprint(sorted_final_movie_pr_rec)

