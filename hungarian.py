def feasible_set(y, edges):
    feasible_edges = {}
    for node in edges:
        feasible_edges[node] = []
        edge_list = y[node]
        for edge in edge_list:
            if edge[1] == y[node] + y[edge[0]]:
                feasible_edges[node].append((edge[0], edge[1]))
    return feasible_edges

def hungarian(A, B, edges, cost):
    M = []
    y = {}
    for a in A:
        y[a] = 0
    for b in B:
        y[b] = 0

    E_y = feasible_set(y, edges)
    