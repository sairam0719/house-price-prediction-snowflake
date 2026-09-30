from snowflake.snowpark.context import get_active_session
import xgboost as xgb

session = get_active_session()

df = session.table(
    "HOUSE_PRICE_DB.ML_SCHEMA.HOUSE_PRICE_TRAIN"
)

data = df.to_pandas()

X = data[
    [
        "X1_TRANSACTION_DATE",
        "X2_HOUSE_AGE",
        "X3_DISTANCE_TO_THE_NEAREST_MRT_STATION",
        "X4_NUMBER_OF_CONVENIENCE_STORES",
        "X5_LATITUDE",
        "X6_LONGITUDE"
    ]
]

y = data["Y_HOUSE_PRICE_OF_UNIT_AREA"]

model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X, y)

print("XGBoost model training completed successfully!")
print("Training rows:", len(data))