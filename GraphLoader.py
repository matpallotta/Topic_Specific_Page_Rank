import csv
import networkx as nx


# load the graoh from input file, and creates a dictionary of edge weights
def graph_loader(input_graph):
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

    return g, dic_node_weight_sum

