import streamlit as st
import snowflake.connector

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 House Price Prediction")
st.write("Predict the house price of unit area using XGBoost and Snowflake.")

st.subheader("Enter Property Details")

transaction_date = st.number_input(
    "Transaction Date",
    value=2013.5,
    step=0.01
)

house_age = st.number_input(
    "House Age",
    min_value=0.0,
    value=10.0,
    step=0.1
)

mrt_distance = st.number_input(
    "Distance to Nearest MRT Station",
    min_value=0.0,
    value=1000.0,
    step=10.0
)

convenience_stores = st.number_input(
    "Number of Convenience Stores",
    min_value=0,
    value=5,
    step=1
)

latitude = st.number_input(
    "Latitude",
    value=24.97,
    format="%.6f"
)

longitude = st.number_input(
    "Longitude",
    value=121.54,
    format="%.6f"
)


if st.button("🔮 Predict House Price"):

    try:

        conn = snowflake.connector.connect(
            account=st.secrets["snowflake"]["account"],
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )

        cursor = conn.cursor()

        query = """
        CALL HOUSE_PRICE_DB.ML_SCHEMA.PREDICT_HOUSE_PRICE_DIRECT(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                transaction_date,
                house_age,
                mrt_distance,
                convenience_stores,
                latitude,
                longitude
            )
        )

        result = cursor.fetchone()

        prediction = float(result[0])

        cursor.close()
        conn.close()

        st.success("Prediction generated successfully!")

        st.metric(
            "Predicted House Price of Unit Area",
            f"{prediction:.2f}"
        )

    except Exception as e:

        st.error("Unable to generate prediction.")

        st.code(str(e))