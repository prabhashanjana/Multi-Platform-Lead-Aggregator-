import pandas as pd
from outputs.sheets import push_to_sheets

df = pd.read_csv("test_data.csv")
print(df.dtypes)
print(df.isnull().sum())
print(df.head())

push_to_sheets(df)
