import nx_parallel as nxp
import numpy as np
def parallel_get_distance_measures(graph):
    max_distance = 0
    avg_distance = 0
    for node, length_dict in nxp.all_pairs_shortest_path_length(graph):
        for k, v in length_dict.items():
            if k == node: continue
            max_distance = max(max_distance, v)
            avg_distance = avg_distance + v #python3 maxint does not have max size, so there shouldnt be an overflow risk.
    nodes = graph.order()
    avg_distance = avg_distance / (nodes * (nodes-1)) #handshake lemma, therefore double-counting of distance is fine.
    return { "diameter" : max_distance,  "avg_distance" : avg_distance }



def parallel_get_betweenness_list(graph):
    betweenness_dict = nxp.betweenness_centrality(graph)
    return np.array( [val for val in betweenness_dict.values()] )