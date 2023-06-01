import queue

INF = 1000000000000000000000000 # infinity

def bfs(node_A, adj_list): 

    # adj_list is a dictionary with adj_list[node] being the list of weighted edges
    # this is for a directed graph, so no change as such adj_list[node] has edges from node->node_2
    path = []
    reachable_nodes = set()
    visited = {}
    parents = {}
    print(adj_list)
    for key in adj_list:
       
        visited[key] = False
    nodes_to_visit = queue.Queue()
    nodes_to_visit.put(node_A)
    while not nodes_to_visit.empty():
        node_visited = nodes_to_visit.get()
        
        visited[node_visited] = True
        reachable_nodes.add(node_visited)
        # process the visited node here
        

        for (v, _) in adj_list[node_visited]:
            if not visited[v]:
                nodes_to_visit.put(v)
                parents[v] = node_visited
    return reachable_nodes


def find_path(node_A, node_B, adj_list):
    path = []
    visited = {}
    parents = {}
    for key in adj_list:
        visited[key] = False
    
    nodes_to_visit = queue.Queue()
    nodes_to_visit.put(node_A)
    while not nodes_to_visit.empty():
        node_visited = nodes_to_visit.get()

        visited[node_visited] = True
        if node_visited == node_B:
            while node_B != node_A:
                path.append(node_B)
                node_B = parents[node_B]
            path.append(node_A)
            path.reverse()
            return path

        for (v, _) in adj_list[node_visited]:
            if not visited[v]:
                nodes_to_visit.put(v)
                parents[v] = node_visited




node_A = 'A'
node_B = 'B'

adj_list = {'A': ['C', 'D', 'E'], 'B': [], 'C': ['B', 'D'], 'D': [], 'E': []}

# implement one iteration of hungarian algorithm

def reachable_set(node_set, adj_list):
    reachable_nodes = set()
    for node in node_set:
        x = bfs(node, adj_list)
        # print(x)
        reachable_nodes = reachable_nodes | x
    # print(reachable_nodes) 
    return reachable_nodes


def add_matching(node_S, node_T, subgraph_matrix, matching, y, original_matrix):
    # matching is the matching uptil now, we need to improve that
    # y is a potential implemented as a dictionary, y[node] gives the potential of the node

    # matching is a list of tuples, giving the matching from node_T to node_S, as a directed graph
    Rs = set()
    Rt = set()
    for pair in matching:
        Rs.add(pair[1])
        Rt.add(pair[0])

    S = set(node_S)
    T = set(node_T)

    Rs = S - Rs
    Rt = T - Rt
    # print(Rs, Rt)
    adj_list = {}
    for u in node_S:
        adj_list[u] = []

    for v in node_T:
        adj_list[v] = []

    for i in range(len(subgraph_matrix)):
        for j in range(len(subgraph_matrix[i])):
            if subgraph_matrix[i][j][0] != INF:
                if subgraph_matrix[i][j][1]:
                    adj_list[node_S[i]].append((node_T[j], subgraph_matrix[i][j][0]))
                else:
                    adj_list[node_T[j]].append((node_S[i], subgraph_matrix[i][j][0]))
    print("adj_list", adj_list)
    Z = reachable_set(Rs, adj_list)
    if len(Z & Rt) == 0:
        # update y, i.e. no edges are tight
        delta = INF
        for i in range(len(original_matrix)):
            for j in range(len(original_matrix[i])):
                delta = min(delta, original_matrix[i][j] - y[node_S[i]] - y[node_T[j]])
        # print(delta)
        # now add this value of delta to all vertices in Z & S and subtract from Z & T
        # print(Z, S, T)
        for node in Z&S:
            y[node] += delta

        for node in Z&T:
            y[node] -= delta

        for i in range(len(original_matrix)):
            for j in range(len(original_matrix[i])):
                if original_matrix[i][j] == y[node_S[i]] + y[node_T[j]]:
                    subgraph_matrix[i][j] = (original_matrix[i][j], True)
        return add_matching(node_S, node_T, subgraph_matrix, matching, y, original_matrix)
    else:


        ####   change this properly 


        # this means there is a path from Rs to Rt using only the edges defined yet, which forms an augmenting path
        for u in Rs:
            for v in bfs(u, adj_list):
            
                path = find_path(u, v, adj_list)
                for i in range(0, len(path)-1, 2):
                    # as path is alternating, the first element is in S, second in T and so on
                    subgraph_matrix[path[i]][path[i+1]] = (subgraph_matrix[path[i]][path[i+1]][0], not subgraph_matrix[path[i]][path[i+1]][1])
                new_matching = []
                for i in range(len(subgraph_matrix)):
                    for j in range(len(subgraph_matrix[i])):
                        if subgraph_matrix[i][j][0] != INF:
                            if subgraph_matrix[i][j][1]:
                                new_matching.append((i, j))
                            else:
                                new_matching.append((j, i))
                return new_matching


node_S = ['a', 'b', 'c']
node_T = ['A', 'B', 'C']

subgraph_matrix = []
for i in range(3):
    row = []
    for j in range(3):
        row.append((INF, True))
    subgraph_matrix.append(row)
# print(subgraph_matrix)
matching = []
y = {'a': 0, 'b': 0, 'c': 0, 'A': 0, 'B': 0, 'C': 0}
original_matrix = [[1, 2, 5], [3, 9, 4], [5, 8, 2]]

print(add_matching(node_S, node_T, subgraph_matrix, matching, y, original_matrix))







