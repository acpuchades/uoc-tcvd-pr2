#!/usr/bin/env python3

from sklearn.manifold import TSNE
from sklearn.pipeline import make_pipeline

from idealista_data import X_train
from data_pipeline import preprocessor

tsne_model = make_pipeline(
    preprocessor,
    TSNE(random_state=123, perplexity=30, max_iter=1000)
)

tsne_results = tsne_model.fit_transform(X_train)
