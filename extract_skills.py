import pandas as pd

input_file = "cleaned_linkedin_data_jobs.csv"
output_file = "linkedin_jobs_with_skills.csv"

df = pd.read_csv(input_file)

skills = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "gcp",
    "spark",
    "hadoop",
    "snowflake",
    "databricks",
    "etl",
    "machine learning",
    "pandas"
]

description_text = df["description"].fillna("").str.lower()

for skill in skills:
    column_name = "skill_" + skill.replace(" ", "_")
    df[column_name] = description_text.str.contains(
        skill,
        regex=False
    )

df.to_csv(output_file, index=False)

print("Skills extracted successfully")
print("Rows:", len(df))
print("Output file:", output_file)

print("\nSkill counts:")
for skill in skills:
    column_name = "skill_" + skill.replace(" ", "_")
    print(skill, ":", df[column_name].sum())