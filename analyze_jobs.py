import pandas as pd

file_path = "linkedin_jobs_with_skills.csv"

df = pd.read_csv(file_path)

print("Total job postings:", len(df))

print("\nTop job titles:")
print(df["title"].value_counts().head(10))

print("\nTop companies:")
print(df["company"].value_counts().head(10))

print("\nTop locations:")
print(df["location"].value_counts().head(10))

skill_columns = [
    "skill_python",
    "skill_sql",
    "skill_excel",
    "skill_power_bi",
    "skill_tableau",
    "skill_aws",
    "skill_azure",
    "skill_gcp",
    "skill_spark",
    "skill_hadoop",
    "skill_snowflake",
    "skill_databricks",
    "skill_etl",
    "skill_machine_learning",
    "skill_pandas"
]

print("\nSkill demand:")
for column in skill_columns:
    skill_name = column.replace("skill_", "").replace("_", " ")
    count = df[column].sum()
    print(skill_name, ":", count)