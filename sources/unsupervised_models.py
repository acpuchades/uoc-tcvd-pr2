#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.pipeline import make_pipeline

from idealista_data import X_train
from data_pipeline import preprocessor

tsne_model = make_pipeline(
    preprocessor,
    TSNE(random_state=123, perplexity=30, max_iter=1000)
)

tsne_results = tsne_model.fit_transform(X_train)

plt.figure(figsize=(8, 6))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1], s=1, alpha=0.5)
plt.title("t-SNE visualization of property features")
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(X_train, x=tsne_results[:, 0], y=tsne_results[:, 1],
                hue='ciudad', palette='Set1', s=3, alpha=0.5, legend=False)
plt.show()
