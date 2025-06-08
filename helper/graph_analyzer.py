import nx_parallel as nxp
import numpy as np
def parallelGetDistanceMeasures(graph):
    maxDistance = 0
    avgDistance = 0
    for node, lengthDict in nxp.all_pairs_shortest_path_length(graph):
        for k, v in lengthDict.items():
            if k == node: continue
            maxDistance = max(maxDistance, v)
            avgDistance = avgDistance + v #python3 maxint does not have max size, so there shouldnt be an overflow risk.
    nodes = graph.order()
    avgDistance = avgDistance / (nodes * (nodes-1)) #handshake lemma, therefore double-counting of distance is fine.
    return { "diameter" : maxDistance,  "avgDistance" : avgDistance }



def parallelGetBetweennessMeasures(graph):
    betweennessDict = nxp.betweenness_centrality(graph)
    data = np.array( [val for val in betweennessDict.values()] )
    min = np.min(data)
    max = np.max(data)
    avg = np.mean(data)
    std = np.std(data)
    return { "min": min, "max": max, "avg": avg, "std": std }

def parallel_get_betweenness_list(graph):
    betweennessDict = nxp.betweenness_centrality(graph)
    return np.array( [val for val in betweennessDict.values()] )