CREATE OR REPLACE PROCEDURE HOUSE_PRICE_DB.ML_SCHEMA.PREDICT_HOUSE_PRICE()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.12'
PACKAGES = (
    'snowflake-snowpark-python',
    'snowflake-ml-python',
    'pandas'
)
HANDLER = 'predict_house_price'
AS
$$
def predict_house_price(session):

    from snowflake.ml.registry import Registry

    registry = Registry(
        session=session,
        database_name="HOUSE_PRICE_DB",
        schema_name="ML_SCHEMA"
    )

    model = registry.get_model("HOUSE_PRICE_XGBOOST")
    mv = model.version("V2")

    stream_df = session.table(
        "HOUSE_PRICE_DB.ML_SCHEMA.HOUSE_PRICE_INCOMING_STREAM"
    )

    data = stream_df.to_pandas()

    if data.empty:
        return "No new records to predict."

    features = [
        "X1_TRANSACTION_DATE",
        "X2_HOUSE_AGE",
        "X3_DISTANCE_TO_THE_NEAREST_MRT_STATION",
        "X4_NUMBER_OF_CONVENIENCE_STORES",
        "X5_LATITUDE",
        "X6_LONGITUDE"
    ]

    X = data[features].copy()

    X["X4_NUMBER_OF_CONVENIENCE_STORES"] = (
        X["X4_NUMBER_OF_CONVENIENCE_STORES"].astype("int8")
    )

    predictions = mv.run(
        X,
        function_name="predict"
    )

    prediction_values = predictions.iloc[:, 0].tolist()

    for i, prediction in enumerate(prediction_values):

        row = data.iloc[i]

        session.sql(
            """
            INSERT INTO HOUSE_PRICE_DB.ML_SCHEMA.HOUSE_PRICE_PREDICTIONS
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            params=[
                float(row["X1_TRANSACTION_DATE"]),
                float(row["X2_HOUSE_AGE"]),
                float(row["X3_DISTANCE_TO_THE_NEAREST_MRT_STATION"]),
                float(row["X4_NUMBER_OF_CONVENIENCE_STORES"]),
                float(row["X5_LATITUDE"]),
                float(row["X6_LONGITUDE"]),
                float(prediction)
            ]
        ).collect()

    return f"Predictions completed for {len(prediction_values)} record(s)."
$$;