import ast
import json
import os
from datetime import datetime, timedelta

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import config
import requests


@dag(
    dag_id="predict_data",
    description="Ingest data from a file to another DAG",
    tags=["dsp", "data_prediction"],
    schedule=timedelta(minutes=4),
    start_date=days_ago(n=0, hour=0),
    catchup=False,
)
def predict_data():
    @task()
    def check_for_new_data():
        folder_path = os.path.join(
            "/home/mdv/dsp-credit-approval/airflow/data/folder_C"
        )
        df_list = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if file.startswith("predicted_"):
                continue
            df = pd.read_csv(file_path)
            df_list.append(df)
            os.rename(file_path, folder_path + "/predicted_" + file)

        if len(df_list) > 0:
            merged_df = pd.concat(df_list, ignore_index=True)
            data_to_ingest_json = merged_df.to_json(orient="records")
            return data_to_ingest_json
        else:
            return None

    @task
    def make_prediction(data_to_ingest_json):
        if data_to_ingest_json is not None:
            df = pd.read_json(data_to_ingest_json, orient="records")
            df["PLATFORM"] = "JOB"

            data = df[
                [
                    "FLAG_OWN_CAR",
                    "FLAG_OWN_REALTY",
                    "AMT_INCOME_TOTAL",
                    "NAME_INCOME_TYPE",
                    "NAME_EDUCATION_TYPE",
                    "NAME_FAMILY_STATUS",
                    "NAME_HOUSING_TYPE",
                    "DAYS_BIRTH",
                    "DAYS_EMPLOYED",
                    "OCCUPATION_TYPE",
                    "CNT_FAM_MEMBERS",
                    "PLATFORM",
                ]
            ].to_dict(orient="records")

            response = requests.post(config.URL_PREDICT, data=json.dumps(data))
            prediction_str = response.json()
            prediction = ast.literal_eval(prediction_str)

            df["DATE_PREDICTED"] = datetime.now().strftime("%Y-%m-%d")
            df["APPROVED"] = prediction

            # Save the predicted data to a new file
            df.to_csv(
                os.path.join(
                    "/home/mdv/dsp-credit-approval/airflow/data/predicted_data.csv"
                ),
                index=False,
            )

    data_json = check_for_new_data()
    make_prediction(data_json)


ingest_data_dag = predict_data()
