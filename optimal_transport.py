import numpy as np
import scipy.optimize

# change of plans, edges will be stored as an adjacency list form, with a dictionary and a list for each node


f = open("/workspaces/optimal_transport/1brr-6v9x.txt", "r")
nodes_A = []
nodes_B = []
edges = {}

def add_edge(node_A, node_B, weight, edges):
    if not node_A in edges:
        edges[node_A] = [(node_B, weight)]
    else:
        for pairs in edges[node_A]:
            if pairs[0] == node_B:
                return
        edges[node_A].append((node_B, weight))


def cost_matrix(edges):
    # takes a set of edges and constructs the cost matrix for the hungarian optimization method
    matrix = []
    for key in edges:
        weights = []
        for pair in edges[key]:
            weights.append(pair[1])
        matrix.append(weights)
    return np.array(matrix)

def optimal_transport(cost_matrix):
    row_ind, col_ind = scipy.optimize.linear_sum_assignment(cost_matrix, True)
    return row_ind, col_ind


for lines in f:
    # (pdb1, chain1, pdb2, chain2, _, _, _, _, TM_score) = lines.split()
    line = lines.split()
    # print("hekk")
    if not line[1] in nodes_A:
        nodes_A.append(line[1])
    if not line[3] in nodes_B:
        nodes_B.append(line[3])
    
    # add_edge((line[1], line[3], line[8]), edges)
    node_A = line[1]
    node_B = line[3]
    weight = float(line[8])
    
    add_edge(node_A, node_B, weight, edges)


    
    # print(lines.split())
# def make_graph(pdb1, pdb2):

print(nodes_A)
print(nodes_B)
print(edges)
print(len(edges))

# print(optimal_transport(cost_matrix(edges)))
print(cost_matrix(edges))
print(optimal_transport(cost_matrix(edges)))










# change of plans, edges will be stored as an adjacency list form, with a dictionary and a list for each node


