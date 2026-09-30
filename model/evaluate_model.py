from snowflake.snowpark.context import get_active_session
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

session = get_active_session()

train_df = session.table(
    "HOUSE_PRICE_DB.ML_SCHEMA.HOUSE_PRICE_TRAIN"
).to_pandas()

test_df = session.table(
    "HOUSE_PRICE_DB.ML_SCHEMA.HOUSE_PRICE_TEST"
).to_pandas()

features = [
    "X1_TRANSACTION_DATE",
    "X2_HOUSE_AGE",
    "X3_DISTANCE_TO_THE_NEAREST_MRT_STATION",
    "X4_NUMBER_OF_CONVENIENCE_STORES",
    "X5_LATITUDE",
    "X6_LONGITUDE"
]

X_train = train_df[features]
y_train = train_df["Y_HOUSE_PRICE_OF_UNIT_AREA"]

X_test = test_df[features]
y_test = test_df["Y_HOUSE_PRICE_OF_UNIT_AREA"]

model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("Model Evaluation Results")
print("MAE:", mae)
print("RMSE:", rmse)
print("R²:", r2)