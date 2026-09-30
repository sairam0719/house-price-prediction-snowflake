# System Architecture

## End-to-End Workflow

The project follows this workflow:

```text
UCI Real Estate Valuation Dataset
            ↓
        Snowflake
            ↓
      Data Preparation
            ↓
       Train / Test Split
            ↓
     XGBoost Regression
            ↓
       Model Evaluation
            ↓
    Snowflake Model Registry
            ↓
      Incoming Property Data
            ↓
        Snowflake Stream
            ↓
      Stored Procedure
            ↓
       Triggered Task
            ↓
     House Price Prediction
            ↓
      Prediction Table

Components
1. Snowflake Database

Stores the project data, training data, test data, incoming records, and predictions.

2. XGBoost

Used as the supervised regression algorithm for predicting house price of unit area.

3. Model Registry

Stores the trained XGBoost model as HOUSE_PRICE_XGBOOST version V2.

4. Stream

Detects new records inserted into the incoming property table.

5. Stored Procedure

Reads new records from the stream and uses the registered model to generate predictions.

6. Triggered Task

Automatically runs the stored procedure when the stream contains new data.

7. Prediction Table

Stores the property information together with the predicted house price.

# Automation Flow

New Property Record
        ↓
Incoming Table
        ↓
Stream Detects New Record
        ↓
Triggered Task Starts
        ↓
Stored Procedure Runs
        ↓
XGBoost V2 Prediction
        ↓
Prediction Stored