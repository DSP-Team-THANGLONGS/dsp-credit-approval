import logging
from datetime import datetime
from datetime import timedelta

import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import os
import glob
import data_validation as dv


@dag(
    dag_id="ingest_data",
    description="Ingest data from a file to another DAG",
    tags=["dsp", "data_ingestion", "data_validation"],
    schedule_interval=timedelta(minutes=2),
    start_date=days_ago(n=0, hour=0),
)
def ingest_data():
    @task
    def get_data_to_ingest_from_local_file():
        nb_rows = 10
        filepath = (
            "/home/mdv/dsp-credit-approval/airflow/data/external_data.csv"
        )
        input_data_df = pd.read_csv(filepath)
        logging.info(f"Extract {nb_rows} rows from the file {filepath}")
        data_to_ingest_df = input_data_df.sample(n=nb_rows)

        # Convert DataFrame to JSON string
        data_to_ingest_json = data_to_ingest_df.to_json(orient="records")

        return data_to_ingest_json

    @task
    def save_data(data_to_ingest_json: pd.DataFrame) -> None:
        data_to_ingest_df = pd.read_json(data_to_ingest_json, orient="records")

        filepath = f'/home/mdv/dsp-credit-approval/airflow/data/folder_A/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        logging.info(f"Ingesting data to the file: {filepath}")
        data_to_ingest_df.to_csv(filepath, index=False)

    @task
    def get_data_validation() -> None:
        directory_path = "/home/mdv/dsp-credit-approval/airflow/data/folder_A"
        success_path = "/home/mdv/dsp-credit-approval/airflow/data/folder_C"
        fail_path = "/home/mdv/dsp-credit-approval/airflow/data/folder_B"
        file_pattern = os.path.join(directory_path, "*.csv")
        file_paths = glob.glob(file_pattern)

        for file_path in file_paths:
            print(file_path)
            if file_path.endswith("data.csv") or os.path.basename(
                file_path
            ).startswith("validated_"):
                continue
            dv.process_file(file_path, fail_path, success_path)

    # Task relationships
    (save_data(get_data_to_ingest_from_local_file()) >> get_data_validation())


ingest_data_dag = ingest_data()
