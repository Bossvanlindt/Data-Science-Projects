# Using the NetworkX library, we create a graph from the input json data and return
# a json containing the top 3 characters by # of edges, sum of weights, & betweenness
import json
import networkx as nx
import argparse
import os

def main(): 
    # Get user input in this format:
    # python compute_network_stats.py -i /path/to/<interaction_network.json> -o /path/to/<stats.json>
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input interaction_network required", required=True)
    parser.add_argument("-o", "--output", help="Output json file required", required=True)
    args = parser.parse_args()
    # Get inputs
    interaction_network = args.input
    output = args.output
    # Create output directory if it doesn't exist
    output = args.output
    if not os.path.exists(os.path.dirname(output)):
        if os.path.dirname(output) != '':
            os.makedirs(os.path.dirname(output))

    # Load the interaction network counts from the json into a dictionary
    with open(interaction_network, 'r') as f:
        interaction_counts = json.load(f)

    # Create the graph from the interaction_network json file
    graph = nx.Graph()
    for name1 in interaction_counts:
        for name2 in interaction_counts[name1]:
            graph.add_edge(name1, name2, weight=interaction_counts[name1][name2])

    # Get the stats and store them in the res dictionary
    res = dict()
    # Most connected by number of edges
    node_degrees = dict()
    for v in graph.nodes():
        node_degrees[v] = graph.degree(v)
    deg_list = list(node_degrees.items())
    deg_list.sort(key=lambda x: x[1], reverse=True)
    res['most_connected_by_num'] = [deg_list[0][0], deg_list[1][0], deg_list[2][0]]
    # Most connected by sum of weight of edges
    node_edge_weights = dict()
    for v in interaction_counts:
        sum = 0
        for k in interaction_counts[v]:
            sum += interaction_counts[v][k]
        node_edge_weights[v] = sum
    weight_list = list(node_edge_weights.items())
    weight_list.sort(key=lambda x: x[1], reverse=True)
    res['most_connected_by_weight'] = [weight_list[0][0], weight_list[1][0], weight_list[2][0]]
    # Most connected by betweenness
    betweenness = nx.betweenness_centrality(graph)
    bet_list = list(betweenness.items())
    bet_list.sort(key=lambda x: x[1], reverse=True)
    res['most_central_by_betweenness'] = [bet_list[0][0], bet_list[1][0], bet_list[2][0]]

    # Save the res dictionary in the output file
    with open(output, 'w') as f:
        f.write(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()