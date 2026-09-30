CREATE OR REPLACE PROCEDURE HOUSE_PRICE_DB.ML_SCHEMA.PREDICT_HOUSE_PRICE_DIRECT(
    TRANSACTION_DATE FLOAT,
    HOUSE_AGE FLOAT,
    MRT_DISTANCE FLOAT,
    CONVENIENCE_STORES FLOAT,
    LATITUDE FLOAT,
    LONGITUDE FLOAT
)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.12'
PACKAGES = (
    'snowflake-snowpark-python',
    'snowflake-ml-python',
    'pandas'
)
HANDLER = 'predict_house_price_direct'
AS
$$

def predict_house_price_direct(
    session,
    transaction_date,
    house_age,
    mrt_distance,
    convenience_stores,
    latitude,
    longitude
):

    import pandas as pd
    from snowflake.ml.registry import Registry

    registry = Registry(
        session=session,
        database_name="HOUSE_PRICE_DB",
        schema_name="ML_SCHEMA"
    )

    model = registry.get_model("HOUSE_PRICE_XGBOOST")
    mv = model.version("V2")

    X = pd.DataFrame([{
        "X1_TRANSACTION_DATE": transaction_date,
        "X2_HOUSE_AGE": house_age,
        "X3_DISTANCE_TO_THE_NEAREST_MRT_STATION": mrt_distance,
        "X4_NUMBER_OF_CONVENIENCE_STORES": convenience_stores,
        "X5_LATITUDE": latitude,
        "X6_LONGITUDE": longitude
    }])

    X["X4_NUMBER_OF_CONVENIENCE_STORES"] = (
        X["X4_NUMBER_OF_CONVENIENCE_STORES"].astype("int8")
    )

    predictions = mv.run(
        X,
        function_name="predict"
    )

    return float(predictions.iloc[0, 0])

$$;