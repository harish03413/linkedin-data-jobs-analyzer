import duckdb

database_file = "job_postings.duckdb"
csv_file = "linkedin_jobs_with_skills.csv"

connection = duckdb.connect(database_file)

connection.execute("""
    CREATE OR REPLACE TABLE job_postings AS
    SELECT *
    FROM read_csv_auto(?)
""", [csv_file])

row_count = connection.execute(
    "SELECT COUNT(*) FROM job_postings"
).fetchone()[0]

connection.close()

print("Data loaded successfully")
print("Rows in database:", row_count)