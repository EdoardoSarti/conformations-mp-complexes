import math
import numpy as np
import scipy.optimize
import copy
from random import random


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


def find_score(row_ind, col_ind, matrix):
    score = 0
    for k in range(len(row_ind)):
        i = row_ind[k]
        j = col_ind[k]
        score += matrix[i][j]

    return score/min(len(row_ind), len(col_ind))


def find_rmsd_score(row_ind, col_ind, matrix):
    score = 0
    for k in range(len(row_ind)):
        i = row_ind[k]
        j = col_ind[k]
        score += matrix[i][j]*matrix[i][j]
    score = score/min(len(row_ind), len(col_ind))
    score = math.sqrt(score)
    return score

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
    score_hopefully_better = find_rmsd_score(row_ind, col_ind, cost_matrix)
    score_naive = find_score(row_ind, col_ind, cost_matrix)
    return row_ind, col_ind, score_naive, score_hopefully_better



for lines in f:
    line = lines.split()
    if not line[1] in nodes_A:
        nodes_A.append(line[1])
    if not line[3] in nodes_B:
        nodes_B.append(line[3])
    
    node_A = line[1]
    node_B = line[3]
    weight = float(line[8])
    
    add_edge(node_A, node_B, weight, edges)

    for key in edges:
        for i in range(len(edges[key]), len(nodes_B)):
            edges[key].append((nodes_B[i], 0))

print(nodes_A)
print(nodes_B)
print(edges)
print(len(edges))

print(cost_matrix(edges))
# print(optimal_transport(cost_matrix(edges)))



def update_matrix(row_ind, col_ind, cost_matrix, eps):
    for k in range(len(row_ind)):
        i = row_ind[k]
        j = col_ind[k]
        cost_matrix[i][j] -= eps

    return cost_matrix
    

# def suboptimal_find(cost_matrix):
#     # essentially find the epsilon
#     l = 0
#     r = 1
#     eps = 0.5
#     row_ind_og, col_ind_og = scipy.optimize.linear_sum_assignment(cost_matrix, True)
#     for i in range(100):
#         print(l, r, eps)
#         matrix = copy.deepcopy(cost_matrix)
#         eps = (l+r)/2
#         for k in range(len(row_ind_og)):
#             i = row_ind_og[k]
#             j = col_ind_og[k]
#             matrix[i][j] -= eps
#         row_ind, col_ind, score = optimal_transport(matrix)
#         # print(matrix)
#         print(row_ind, col_ind, score, row_ind_og, col_ind_og)
#         if (row_ind == row_ind_og).all() and (col_ind == col_ind_og).all():
#             print("hello")
#             l = eps 
#         else:
#             r = eps
    
#     return row_ind, col_ind, find_score(row_ind, col_ind, cost_matrix), eps
    

def suboptimal_find(cost_matrix, eps):
    matrix = copy.deepcopy(cost_matrix)
    for i in range(10):
        row_ind, col_ind, score_naive, score_hopefully_better = optimal_transport(matrix)

        for k in range(len(row_ind)):
            i = row_ind[k]
            j = col_ind[k]
            matrix[i][j] -= eps

    row_ind, col_ind, score_naive, score_hopefully_better = optimal_transport(matrix)
    score_naive = find_score(row_ind, col_ind, cost_matrix)
    score_hopefully_better = find_rmsd_score(row_ind, col_ind, cost_matrix)
    return row_ind, col_ind, score_naive, score_hopefully_better



print(optimal_transport(cost_matrix(edges)))
print(suboptimal_find(cost_matrix(edges), 0.008))
# print(suboptimal_find(cost_matrix(edges)))








