# Network Modeling of the Interactions Between Ponies in My Little Ponies

The build_interaction_network.py script computes the number of interactions between every pony in the script and saves them to the interaction_network.json file. 

compute_network_stats.py then takes that file, builds a graph using the NetworkX library, and outputs the stats.json file containing the top pony connections according to different metrics. 