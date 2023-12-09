import pandas as pd

file_path_records = '../data/records.csv'

df_records = pd.read_csv(file_path_records)

own_car_total_count = df_records['own_car'].count()
own_car_unique_count = df_records['own_car'].nunique()

own_realty_total_count = df_records['own_realty'].count()
own_realty_unique_count = df_records['own_realty'].nunique()

print(f"Total count of values in 'own_car' column: {own_car_total_count}")
print(f"Unique count of values in 'own_car' column: {own_car_unique_count}\n")

print(f"Total count of values in 'own_realty' column: {own_realty_total_count}")
print(f"Unique count of values in 'own_realty' column: {own_realty_unique_count}")

