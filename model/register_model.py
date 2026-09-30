from snowflake.snowpark.context import get_active_session
from snowflake.ml.registry import Registry
import xgboost as xgb

session = get_active_session()

train_df = session.table(
    "HOUSE_PRICE_DB.ML_SCHEMA.HOUSE_PRICE_TRAIN"
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

model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

registry = Registry(
    session=session,
    database_name="HOUSE_PRICE_DB",
    schema_name="ML_SCHEMA"
)

model_version = registry.log_model(
    model,
    model_name="HOUSE_PRICE_XGBOOST",
    version_name="V2",
    sample_input_data=X_train.head(5),
    target_platforms=["WAREHOUSE"],
    comment="XGBoost house price regression model - Warehouse inference"
)

print("Model registered successfully!")
print("Model: HOUSE_PRICE_XGBOOST")
print("Version: V2")