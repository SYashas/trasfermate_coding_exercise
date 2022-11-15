import pandas as pd

df1 = pd.read_json('file1.json')
print(df1)

df2 = pd.read_json('file2.json')
# print(df2)

if set(df1.columns.values) != set(df2.columns.values):
    raise ValueError('Different columns in 2 datasets')

df3 = pd.concat([df1, df2])
# print(df3)

df3.to_csv('coverted_json.csv', index=False)

df4 = pd.read_csv('coverted_json.csv')
print('Result')
print(df4)