from datetime import timedelta

import os
import glob

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import sys

sys.path.append("../../")
import data_validation as dv


@dag(
    dag_id="validate_data",
    description="Validate data from a file to another DAG",
    tags=["dsp", "data_validation"],
    schedule=timedelta(minutes=2),
    start_date=days_ago(n=0, hour=1),
)
def validate_data():
    @task
    def get_data_validation() -> str:
        directory_path = (
            "/home/mdv/dsp-credit-approval/airflow/data/split_data"
        )
        success_path = (
            "/home/mdv/dsp-credit-approval/airflow/data/validated_data/success"
        )
        fail_path = (
            "/home/mdv/dsp-credit-approval/airflow/data/validated_data/fail"
        )
        file_pattern = os.path.join(directory_path, "*.csv")
        file_paths = glob.glob(file_pattern)

        for file_path in file_paths:
            dv.process_file(file_path, fail_path, success_path)

    get_data_validation()


validate_data_dag = validate_data()
