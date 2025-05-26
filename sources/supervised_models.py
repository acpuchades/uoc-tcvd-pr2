#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, r2_score

from idealista_data import X_train, y_train, X_test, y_test
from data_pipeline import preprocessor, boxcox_transform, inv_boxcox_transform

dt_model = make_pipeline(
  preprocessor,
  DecisionTreeRegressor(max_depth=10, random_state=123),
)

dt_model_t = TransformedTargetRegressor(
    regressor=dt_model,
    func=boxcox_transform(1/4),
    inverse_func=inv_boxcox_transform(1/4)
)

dt_model_t.fit(X_train, y_train)
y_pred = dt_model_t.predict(X_test)

print("RMSE:", root_mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

gbr_model = make_pipeline(
  preprocessor,
  HistGradientBoostingRegressor(max_iter=1000, learning_rate=0.1,
                                max_depth=10, random_state=123),
)

gbr_model_t = TransformedTargetRegressor(
    regressor=gbr_model,
    func=boxcox_transform(1/4),
    inverse_func=inv_boxcox_transform(1/4)
)

gbr_model_t.fit(X_train, y_train)
y_pred = gbr_model_t.predict(X_test)

print("RMSE:", root_mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

plt.figure(figsize=(6, 4))
plt.scatter(x=y_pred, y=y_test, s=3, alpha=0.2)
plt.axline((0, 0), (1, 1), color='gray', linestyle='--')
plt.xlabel("Predicción del precio/m2")
plt.ylabel("Precio/m2 real")
plt.show()

y_resid = y_test - y_pred

plt.figure(figsize=(6, 4))
sns.scatterplot(x=y_pred, y=y_resid, s=3, alpha=0.5)
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("Predicted price/m²")
plt.ylabel("Residual")
plt.title("Residuals vs. Predicted")
plt.tight_layout()
plt.show()
