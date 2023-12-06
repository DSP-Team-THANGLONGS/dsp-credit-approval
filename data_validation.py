import great_expectations as ge
import shutil
import os
import pandas as pd
from datetime import datetime
from pyteamcity import TeamCity

'''
data = pd.read_csv('dsp-credit-approval/data/application_record.csv')
print(data.head())
'''
def read_and_validate_file(file_path):
    context = ge.data_context.DataContext('great-expectations')  

    batch = context.get_batch(file_path)

    validation_result = batch.validate()

    return validation_result

def process_file(file_path, folder_a, folder_b, folder_c):
    validation_result = read_and_validate_file(file_path)

    if validation_result["success"]:
        store_file_in_folder(file_path, folder_c)
    else:
        if all(result['success'] is False for result in validation_result['results']):
            store_file_in_folder(file_path, folder_b)

            save_data_problems_statistics(validation_result)

        else:
            split_file_and_save_problems(file_path, folder_b, folder_c, validation_result)

    if not validation_result["success"]:
        alert_user_with_teams_notification()

def store_file_in_folder(file_path, destination_folder):
    shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))

def save_data_problems_statistics(validation_result):
    
    pass

def split_file_and_save_problems(file_path, folder_b, folder_c, validation_result):
    
    pass

def alert_user_with_teams_notification():
    teamcity = TeamCity()
    teamcity.post_message("Data quality issues detected. Check the logs for details.")

# Example Usage
file_to_process = "dsp-credit-approval/data/application_record.csv"
folder_A = "dsp-credit-approval/great-expectations/folder_A"
folder_B = "dsp-credit-approval/great-expectations/folder_B"
folder_C = "dsp-credit-approval/great-expectations/folder_C"

process_file(file_to_process, folder_A, folder_B, folder_C)
