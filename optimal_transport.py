import numpy as np
import scipy.optimize
import copy
from random import random
# change of plans, edges will be stored as an adjacency list form, with a dictionary and a list for each node


f = open("/workspaces/optimal_transport/test_file.txt", "r")
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
    score = 0
    for k in range(len(row_ind)):
        i = row_ind[k]
        j = col_ind[k]
        score += cost_matrix[i][j]
    return row_ind, col_ind, score



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


###########################################################################################################################################################################


#Now for the tweaks, we want to tweak a little bit in this optimal matching and get a close enough solution

# for an nxn matrix 

def suboptimal_find(cost_matrix):
    matrix = copy.deepcopy(cost_matrix)
    for i in range(10):
        row_ind, col_ind, score = optimal_transport(matrix)
        for k in range(len(row_ind)):
            i = row_ind[k]
            j = col_ind[k]
            matrix[i][j] -= 0.008

    row_ind, col_ind, score = optimal_transport(matrix)
    score = 0
    for k in range(len(row_ind)):
        i = row_ind[k]
        j = col_ind[k]
        score += cost_matrix[i][j]
    return row_ind, col_ind, score


print(suboptimal_find(cost_matrix(edges)))

# l = []
# for i in range(10):
#     l2 = []
#     for j in range(10):
#         l2.append(random())
#     l.append(l2)

# print(optimal_transport())

# print(optimal_transport(suboptimal_find(np.array(l))))





