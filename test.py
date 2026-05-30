import pandas as pd

data = pd.read_csv("Data/crop_data.csv")

print("\n FIRST 5 ROWS:")
print(data.head())

print("\n PRINT COLUMN NAMES:")
print(data.columns)

print("\n DATASET INFO:")
print(data.info())

print("\n MISSING VALUES INFO:")
print(data.isnull().sum())

print("\n DUPLICATE ROWS:")
print(data.duplicated().sum())

#removing duplicate rows
data = data.drop_duplicates()

print("\n AFTER REMOVING DUPLICATES:")
print(data.shape)

data.to_csv("data/cleared_crop_data.csv",index=False)

print("\nCLEANED DATA SAVED SUCCESSFULLY")