# here we use the data to perform hierarchical clustering

#  fetching the matrix

from sklearn.cluster import SpectralClustering
from sklearn.cluster import KMeans
import numpy as np

import sys
def laplacian(matrix):
    n = len(matrix)
    D = []
    for i in range(n):
        dj = 0
        row = [0]*n
        for j in range(n):
            dj += matrix[i][j]
        row[i] = dj
        D.append(row)

    return np.array(D) - np.array(matrix)

n = 191 # number of proteins
f = open("./tmp/data.txt", "r")       # Change this file location
lines = []
for line in f:
    line = line.strip()
    line = line.split("-")
    lines.append(line)


protein_map = {}

similarity_matrix = []
for i in range(n):
    row = []
    protein_map[i] = lines[n*i][0]
    for j in range(n):
        if lines[n*i+j][2] == "0 0":
            lines[n*i+j][2] = "0"
        if lines[n*i+j][2] == "":
            lines[n*i+j][2] = 0
        
        row.append(float(lines[n*i+j][2]))
    similarity_matrix.append(row)

# print(similarity_matrix)

print(protein_map)

# sc = SpectralClustering(similarity_matrix).labels_
print(similarity_matrix)
eigen_values, eigen_vectors = np.linalg.eig(laplacian(np.array(similarity_matrix))) # finding the eigenvalues and eigenvectos

eigen_val_vec = []

for i in range(len(eigen_values)):
    eigen_val_vec.append((eigen_values[i], eigen_vectors[i]))

eigen_values.sort()

print(eigen_values)
eigen_val_vec.sort()
# print(eigen_val_vec)
def find_k(eigen_val_vec):
    k_vectors = []
    for i in range(len(eigen_val_vec)-1):
        if eigen_val_vec[i+1][0] - eigen_val_vec[i][0] < 1e-3:
            k_vectors.append(eigen_val_vec[i][1])
        else:
            k_vectors.append(eigen_val_vec[i][1])
            break
    return k_vectors

X = np.array(find_k(eigen_val_vec))

X = X.T

### X is the set of 191 points in 3 Dimensions

kmeans = KMeans(n_clusters = 3, random_state = 0, n_init = "auto").fit(X)
labels = kmeans.labels_

X_0 = []
X_1 = []
X_2 = []

for i in range(len(labels)):
    if labels[i] == 0:
        X_0.append(X[i])
    elif labels[i] == 1:
        X_1.append(X[i])
    else:X_2.append(X[i])

X_0 = np.array(X_0)
X_1 = np.array(X_1)
X_2 = np.array(X_2)

# print(l)
# dict = {}
# for i in range(len(l)):
#     x = l[i]
#     if not(x in dict):
#         dict[x] = [protein_map[i]]
#     else:
#         dict[x].append(protein_map[i])

# print(dict)












