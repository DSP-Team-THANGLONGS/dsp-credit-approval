pip install pandas 

import pandas as pd

file_path = 'data\data_problems_statistics.csv'
column_name = 'column'

df = pd.read_csv(file_path)

total_count = df[column_name].nunique()

print(f"Total count of unique values in {column_name}: {total_count}")
