from datetime import timedelta
import os
import glob
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import data_validation as dv


@dag(
    dag_id="validate_data",
    description="Validate data from a file to another DAG",
    tags=["dsp", "data_validation"],
    schedule=timedelta(minutes=3),
    start_date=days_ago(n=0, hour=0),
)
def validate_data():
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

    get_data_validation()


validate_data_dag = validate_data()
