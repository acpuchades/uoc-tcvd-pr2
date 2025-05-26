#!/usr/bin/env python3

from idealista_data import X_train, y_train, X_test, y_test
from data_pipeline import preprocessor, boxcox_transform, inv_boxcox_transform

from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error, r2_score

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
