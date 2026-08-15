import pandas as pd

file_path = "cleaned_linkedin_data_jobs.csv"

df = pd.read_csv(file_path)

print("Rows:", len(df))
print("Columns:", df.columns.tolist())
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nFirst 5 rows:")
print(df.head())