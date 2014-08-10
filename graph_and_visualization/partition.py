import networkx as nx
from networkx.readwrite import json_graph
import community
 
# graph io in json format
def read_json_file(filename):
    graph = json_graph.load(open(filename))
    print "Read in file", filename
    print nx.info(graph).replace("\n"," | ")
    return graph
 
def save_to_jsonfile(graph, filename):
    g=graph
    g_json=json_graph.node_link_data(g)
    json_graph.dump(g_json, open(filename,'w'))
 
# network partition that maximizes the modularity using Louvain heuristic
def assign_community(graph):
    g=nx.Graph(graph)
    partition=community.best_partition(g)
    print "Partition found: ",len(set(partition.values()))
    for n in g.nodes_iter():
        g.node[n]["partition"]=partition[n]
    return g
     
   
