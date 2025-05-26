#!/usr/bin/env python3

import numpy as np

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_features = ['superficie', 'habitaciones']
categorical_features = [
  'piso', 'ascensor', 'exterior', 'garaje', 'terraza',
  'calle', 'barrio', 'distrito', 'ciudad', 'provincia'
]

def boxcox_transform(lam):
    return lambda x: (np.power(x, lam) - 1) / lam

def inv_boxcox_transform(lam):
    return lambda y: np.power((lam * y) + 1, 1 / lam)

preprocessor = make_column_transformer(
  (StandardScaler(), numeric_features),
  (OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
)
