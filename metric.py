# from perfect_matchings import *
import scipy.optimize
import numpy as np
import math
f = open("test_file.txt", "r")
nodes_A = []
nodes_B = []
adj_list = {}

for lines in f:
    line = lines.split()
    if not line[1] in nodes_A:
        nodes_A.append(line[1])
        adj_list[line[1]] = []

    if not line[3] in nodes_B:
        nodes_B.append(line[3])
        adj_list[line[3]] = []

    node_A = line[1]
    node_B = line[3]
    weight = float(line[8])
    adj_list[node_A].append((node_B, weight))
    adj_list[node_B].append((node_A, weight))
    

node_to_index_map = {}
for i in range(len(nodes_A)):
    node_to_index_map[nodes_A[i]] = i

for j in range(len(nodes_B)):
    node_to_index_map[nodes_B[j]] = j

original_matrix = []

for i in range(len(nodes_A)):
    row = []
    for j in range(len(nodes_B)):
        if j < len(adj_list[nodes_A[i]]):
            row.append(adj_list[nodes_A[i]][j][1])
        else:
            row.append(0)
    original_matrix.append(row)


while len(nodes_A) < len(nodes_B):
    row = []
    for i in range(len(nodes_B)):
        row.append(0)

    original_matrix.append(row)
    nodes_A.append("$" + str(i))

while len(nodes_B) < len(nodes_A):
    
    for i in range(len(nodes_A)):
        for j in range(len(nodes_A) - len(nodes_B)):
            original_matrix[i].append(0)

    nodes_B.append("$" + str(len(nodes_A)-len(nodes_B)))


# nodes_A = ['a', 'b', 'c', '$']
# nodes_B = ['A', 'B', 'C', 'D']
# original_matrix = [[0.9781, 0.9781, 0.9781, 0], [0.9782, 0.9782, 0.9782, 0], [0.9795, 0.9795, 0.9795, 0], [0.87, 0, 0, 0]]


# print(original_matrix)


def f(x):
    return x*x

def modified_max(f, original_matrix):
    print(original_matrix)
    for i in range(len(original_matrix)):
        for j in range(len(original_matrix[i])):
            original_matrix[i][j] = f(original_matrix[i][j])

    


    if original_matrix == []:
        print(0, 0)

    else:
        row_ind, col_ind = scipy.optimize.linear_sum_assignment(np.array(original_matrix), True)
        score = 0
        num_considered = 0
        for i in range(len(row_ind)):
            num_considered += 1
            score += original_matrix[row_ind[i]][col_ind[i]]
            print(original_matrix[row_ind[i]][col_ind[i]])
        score = score/num_considered
        score = math.sqrt(score)
        print(score)


modified_max(f, original_matrix)