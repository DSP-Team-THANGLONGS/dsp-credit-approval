import ast
import datetime
import glob
import json
import logging
import os
from datetime import datetime
from datetime import timedelta

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

import config

import requests
import data_validation as dv


@dag(
    dag_id="predict_data",
    description="Ingest data from a file to another DAG",
    tags=["dsp", "data_prediction"],
    schedule=timedelta(minutes=4),
    start_date=days_ago(n=0, hour=0),
)
def predict_data():
    @task()
    def check_for_new_data():
        folder_path = (
            "/home/mdv/dsp-credit-approval/airflow/data/validated_data/success"
        )
        df_list = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and file.endswith(".csv"):
                df = pd.read_csv(file_path)
                df_list.append(df)

        merged_df = pd.concat(df_list, ignore_index=True)
        data_to_ingest_json = merged_df.to_json(orient="records")
        return data_to_ingest_json

    @task
    def make_prediction(data_to_ingest_json: pd.DataFrame):
        df = pd.read_json(data_to_ingest_json, orient="records")
        data = []
        for _, row in df.iterrows():
            data.append(
                {
                    "FLAG_OWN_CAR": row["FLAG_OWN_CAR"],
                    "FLAG_OWN_REALTY": row["FLAG_OWN_REALTY"],
                    "AMT_INCOME_TOTAL": row["AMT_INCOME_TOTAL"],
                    "NAME_INCOME_TYPE": row["NAME_INCOME_TYPE"],
                    "NAME_EDUCATION_TYPE": row["NAME_EDUCATION_TYPE"],
                    "NAME_FAMILY_STATUS": row["NAME_FAMILY_STATUS"],
                    "NAME_HOUSING_TYPE": row["NAME_HOUSING_TYPE"],
                    "DAYS_BIRTH": row["DAYS_BIRTH"],
                    "DAYS_EMPLOYED": row["DAYS_EMPLOYED"],
                    "OCCUPATION_TYPE": row["OCCUPATION_TYPE"],
                    "CNT_FAM_MEMBERS": row["CNT_FAM_MEMBERS"],
                    "PLATFORM": "Job",
                }
            )
        response = requests.post(config.URL_PREDICT, data=json.dumps(data))
        prediction_str = response.json()
        prediction = ast.literal_eval(prediction_str)
        df["DATE_PREDICTED"] = datetime.now().strftime("%Y-%m-%d")
        df["APPROVED"] = prediction
        filepath = f'/home/mdv/dsp-credit-approval/airflow/data/predicted_data/{datetime.now().strftime("%Y-%M-%d_%H-%M-%S")}.csv'
        logging.info(f"Predicted data to the file: {filepath}")
        df.to_csv(filepath, index=False)

    df_merged = check_for_new_data()
    make_prediction(df_merged)


ingest_data_dag = predict_data()
