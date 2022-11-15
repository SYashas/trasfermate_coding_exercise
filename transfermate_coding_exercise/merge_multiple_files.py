import os
import pandas as pd

path = '/Users/yashas/Documents/transfermate_coding_exercise/sales_records'

files = [path + f for f in os.listdir(path)]

csv_list = []

for file in files:
    csv_list.append(pd.read_csv(file).assign(File_Name = os.path.basename(file)))

csv_merged = pd.concat(csv_list, ignore_index=True)

csv_merged.to_csv(path + 'sales_records_full.csv', index=False)

