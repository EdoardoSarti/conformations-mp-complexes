import numpy as np
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

data = load_digits().data
pca = PCA(2)

df = pca.fit_transform(data)

print(df.shape)

kmeans = KMeans(10)

label = kmeans.fit_predict(df)
filtered_label0 = df[label == 0]
plt.scatter(filtered_label0[:,0], filtered_label0[:, 1])
plt.show()
print(label)

