# House Price Prediction using Snowflake and XGBoost

## Project Overview

This project predicts house prices using machine learning and Snowflake.

The project uses the UCI Real Estate Valuation dataset and an XGBoost Regression model. The complete machine learning workflow is implemented using Snowflake for data storage, model management, and automated prediction.

## Machine Learning

- Learning Type: Supervised Learning
- ML Task: Regression
- Algorithm: XGBoost Regressor
- Target: House Price of Unit Area

## Dataset

Dataset: Real Estate Valuation

Source: UCI Machine Learning Repository

The dataset contains 414 records and 6 input features.

### Features

- Transaction Date
- House Age
- Distance to the Nearest MRT Station
- Number of Convenience Stores
- Latitude
- Longitude

### Target

House Price of Unit Area

## Model Performance

- MAE: 4.66
- RMSE: 7.26
- R²: 0.73

## Technology Stack

- Python
- Snowflake
- Snowpark Python
- XGBoost
- Pandas
- Snowflake Model Registry
- Snowflake Streams
- Snowflake Tasks
- SQL

## Project Workflow

Dataset → Snowflake → Data Preparation → Train/Test Split → XGBoost Training → Model Evaluation → Model Registry → Incoming Data → Stream → Stored Procedure → Triggered Task → House Price Prediction

## Automation

New property records are inserted into the incoming table.

A Snowflake Stream detects new records.

A Triggered Task automatically calls the prediction stored procedure.

The registered XGBoost model generates the predicted house price.

The prediction is stored in the prediction table.

## Project Structure

```text
house-price-prediction-snowflake/
├── README.md
├── data/
├── sql/
├── model/
├── results/
└── docs/