import pandas as pd

# Load the CSV file
df = pd.read_csv("linkedin_data_jobs.csv")

# Show column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# Show first 5 rows
print("\nFIRST 5 ROWS:")
print(df.head())

# Show information about the dataset
print("\nDATASET INFORMATION:")
print(df.info())