import pandas as pd

# Read the CSV using the Python parser
df = pd.read_csv(
    "linkedin_data_jobs.csv",
    engine="python"
)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nDATASET INFORMATION:")
df.info()
