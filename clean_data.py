import pandas as pd

input_file = "linkedin_data_jobs.csv"
output_file = "cleaned_linkedin_data_jobs.csv"

df = pd.read_csv(input_file)

print("Rows before cleaning:", len(df))

df = df.drop_duplicates()

text_columns = [
    "title",
    "company",
    "location",
    "description"
]

for column in text_columns:
    df[column] = df[column].fillna("").astype(str).str.strip()

df = df[
    (df["title"] != "") &
    (df["description"] != "")
]

df["date_posted"] = pd.to_datetime(
    df["date_posted"],
    errors="coerce"
)

df.to_csv(output_file, index=False)

print("Rows after cleaning:", len(df))
print("Cleaned file saved to:", output_file)