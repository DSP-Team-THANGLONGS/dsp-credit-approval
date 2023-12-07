import glob
import json
from datetime import timedelta
import os

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
    schedule=timedelta(minutes=2),
    start_date=days_ago(n=0, hour=1),
)
def predict_data():
    @task
    def data_prediction() -> str:
        directory_path = (
            "/home/mdv/dsp-credit-approval/airflow/data/validated_data/success"
        )
        predicted_path = (
            "/home/mdv/dsp-credit-approval/airflow/data/predicted_data/"
        )
        file_pattern = os.path.join(directory_path, "*.csv")
        file_path = glob.glob(file_pattern)[0]
        df = pd.read_csv(file_path)
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
        print(response)
        dv.store_file_in_folder(file_path, predicted_path)

    data_prediction()


ingest_data_dag = predict_data()
