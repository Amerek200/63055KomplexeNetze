import nx_parallel as nxp
import networkx as nx
import numpy as np
import powerlaw

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

def get_powerlaw_result(degree_list):
    result = powerlaw.Fit(degree_list)
    return result.alpha, result.xmin

def find_word_regiment_candidates(deg_prob_dict, start=10, stop=0, step=10, max_diff=5):
    print(str.format("unterschiedliche Knotengrade im Dictionary: {0}", len(deg_prob_dict)))
    sorted_tuple_list = [(deg, deg_prob_dict[deg]) for deg in sorted(deg_prob_dict.keys())]
    print(sorted_tuple_list)
    res = dict()
    for i in range(start, stop if stop != 0 else len(sorted_tuple_list), step):
        left = sorted_tuple_list[:i]
        right = sorted_tuple_list[i:]
        deg_left = [t[1] for t in left]
        deg_right = [t[1] for t in right]
        try:
            powerlaw_left = powerlaw.Fit(deg_left, xmin = min(deg_left) )
            powerlaw_right = powerlaw.Fit(deg_right, xmin= (min(deg_right)))
            #if np.isinf(powerlaw_left.alpha) or np.isinf(powerlaw_right.alpha): continue
            res[i] = { "left": powerlaw_left.alpha, "right": powerlaw_right.alpha}
        except Exception as e:
            print(f"Skipping {i} due to error: {e}")
            continue
    
    #sort by difference between left-right regmiment, desc
    res = dict(filter(lambda item: abs(item[1]["left"] - item[1]["right"]) <= max_diff, res.items()))
    res = dict(sorted(
        res.items(), 
        key=lambda item: abs(item[1]["left"] - item[1]["right"]),
        reverse=True
        ))
    return res
	
def get_deg_probability_dict(graph):
    deg_frequency_list = np.array(nx.degree_histogram(graph))
    total_nodes = graph.order()
    res = {}
    for deg in range(len(deg_frequency_list)):
        if deg_frequency_list[deg] == 0: continue
        else:
            res[deg] = deg_frequency_list[deg] / total_nodes
    return res

def hello():
    print("HI")
