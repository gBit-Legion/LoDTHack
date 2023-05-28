import re
import nltk
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import string

import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

class MlModel():
    def mbkmeans_clusters(self, X, k, mb=500, print_silhouette_values=False):

        km = MiniBatchKMeans(n_clusters=k, batch_size=mb).fit(X)
        print(f"For n_clusters = {k}")
        print(f"Silhouette coefficient: {silhouette_score(X, km.labels_):0.2f}")
        print(f"Inertia:{km.inertia_}")

        if print_silhouette_values:
            sample_silhouette_values = silhouette_samples(X, km.labels_)
            print(f"Silhouette values:")
            silhouette_values = []
            for i in range(k):
                cluster_silhouette_values = sample_silhouette_values[km.labels_ == i]
                silhouette_values.append(
                    (
                        i,
                        cluster_silhouette_values.shape[0],
                        cluster_silhouette_values.mean(),
                        cluster_silhouette_values.min(),
                        cluster_silhouette_values.max(),
                    )
                )
            silhouette_values = sorted(
                silhouette_values, key=lambda tup: tup[2], reverse=True
            )
            for s in silhouette_values:
                print(
                    f"    Cluster {s[0]}: Size:{s[1]} | Avg:{s[2]:.2f} | Min:{s[3]:.2f} | Max: {s[4]:.2f}"
                )
        return km, km.labels_

    def model_quality_assessment(self, prep_data):
        kmeans_kwargs = {
            "init": "random",
            "n_init": 10,
            "random_state": 1,
        }

        # create list to hold SSE values for each k
        sse = []
        for k in range(1, 11):
            kmeans = MiniBatchKMeans(n_clusters=k, batch_size=1000, **kmeans_kwargs)
            kmeans.fit(prep_data['vectors'].tolist())
            sse.append(kmeans.inertia_)

        # visualize results
        plt.plot(range(1, 11), sse)
        plt.xticks(range(1, 11))
        plt.xlabel("Number of Clusters")
        plt.ylabel("SSE")
        plt.show()
