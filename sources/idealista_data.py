#!/usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split

datos = pd.read_csv("output/idealista-sale-properties-spain_processed.csv")
datos = datos[~datos.price_m2.isna()]

datos_X = datos[[
  "superficie", "habitaciones", "piso", "ascensor", "exterior", "garaje",
  "calle", "barrio", "distrito", "ciudad", "provincia",
  "energy_consumption", "energy_emissions",
]]

datos_y = datos["price_m2"]

X_train, X_test, y_train, y_test = train_test_split(
    datos_X, datos_y, test_size=0.2, random_state=1234
)
