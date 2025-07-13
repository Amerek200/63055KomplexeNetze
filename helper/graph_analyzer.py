import nx_parallel as nxp
import networkx as nx
import numpy as np
import powerlaw
from scipy.stats import linregress

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

def find_word_regiment_candidates(deg_prob_dict, start=10, step=10):
    sorted_tuple_list = [(deg, deg_prob_dict[deg]) for deg in sorted(deg_prob_dict.keys())]
    res = dict()
    for i in range(start, len(sorted_tuple_list), step):
        left = sorted_tuple_list[:i]
        right = sorted_tuple_list[i:]
        deg_left = [t[1] for t in left]
        deg_right = [t[1] for t in right]
        powerlaw_left = powerlaw.Fit(deg_left, xmin = min(deg_left) )
        powerlaw_right = powerlaw.Fit(deg_right, xmin= (min(deg_right)))
        res[i] = { "left": powerlaw_left.alpha, "right": powerlaw_right.alpha}
    #sort by difference between left-right regmiment, desc
    res = dict(sorted(
        res.items(), 
        key=lambda item: abs(item[1]["left"] - item[1]["right"]),
        reverse=True
        ))
    return res
	
def getDegProbabilityDict(graph):
    deg_frequency_list = np.array(nx.degree_histogram(graph))
    total_nodes = graph.order()
    res = {}
    for deg in range(len(deg_frequency_list)):
        if deg_frequency_list[deg] == 0: continue
        else:
            res[deg] = deg_frequency_list[deg] / total_nodes
    return res

def approx_exponent_first_five_groups(graph, min_deg=2):
    deg_prob_dict = get_deg_probability_dict(graph)
    deg_prob_dict = { k: v for k, v in deg_prob_dict.items() if k >= min_deg }
    grouped = group_by_power_of_two(deg_prob_dict)
    lowest_five_keys = sorted(grouped.keys())[:5]
    grouped = { k : grouped[k] for k in lowest_five_keys }
    lin_reg_results = lin_reg_on_grouped_deg_prob_dict(grouped)
    return lin_reg_results

def group_by_power_of_two(deg_prob_dict, group_method="lower"):
    max_deg = max(deg_prob_dict.keys())
    bucket_dict = dict()
    for deg, prob in deg_prob_dict.items():
        if group_method == "lower":
            bucket = 2 ** int(np.floor(np.log2(deg)))
        elif group_method == "upper":
            bucket = 2 ** int(np.ceil(np.log2(deg)))
        #print(str.format("deg: {0}, bin: {1}", deg, bucket))
        if bucket not in bucket_dict:
            bucket_dict[bucket] = prob
        else:
            bucket_dict[bucket] = bucket_dict[bucket] + prob
    return bucket_dict
	
def get_deg_probability_dict(graph):
    deg_frequency_list = np.array(nx.degree_histogram(graph))
    total_nodes = graph.order()
    res = {}
    for deg in range(len(deg_frequency_list)):
        if deg_frequency_list[deg] == 0: continue
        else:
            res[deg] = deg_frequency_list[deg] / total_nodes
    return res

def lin_reg_on_grouped_deg_prob_dict(grouped_dict):
    sorted_dict = dict(sorted(grouped_dict.items()))
    x_values = np.log10(list(sorted_dict.keys()))
    y_values = np.log10(list(sorted_dict.values()))
    lin_reg_results = linregress(x_values, y_values)
    # results contain: slope, intercept (y-axis cutting point), rvalue, pvalue, stderr
    return lin_reg_results
