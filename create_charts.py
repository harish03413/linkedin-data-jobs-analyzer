import duckdb
import matplotlib.pyplot as plt

connection = duckdb.connect("job_postings.duckdb")

result = connection.execute("""
    SELECT
        title,
        COUNT(*) AS job_count
    FROM job_postings
    WHERE title IS NOT NULL
    GROUP BY title
    ORDER BY job_count DESC
    LIMIT 10
""").fetchdf()

plt.figure(figsize=(10, 6))
plt.barh(result["title"][::-1], result["job_count"][::-1])
plt.xlabel("Number of job postings")
plt.ylabel("Job title")
plt.title("Top 10 LinkedIn Data Job Titles")
plt.tight_layout()
plt.savefig("top_job_titles.png", dpi=150)
plt.close()

skills = {
    "SQL": "skill_sql",
    "Python": "skill_python",
    "Excel": "skill_excel",
    "Power BI": "skill_power_bi",
    "Tableau": "skill_tableau",
    "AWS": "skill_aws",
    "Machine Learning": "skill_machine_learning"
}

skill_names = []
skill_counts = []

for name, column in skills.items():
    count = connection.execute(
        f"SELECT SUM(CAST({column} AS INTEGER)) FROM job_postings"
    ).fetchone()[0]

    skill_names.append(name)
    skill_counts.append(count)

plt.figure(figsize=(10, 6))
plt.bar(skill_names, skill_counts)
plt.xlabel("Skill")
plt.ylabel("Number of job postings")
plt.title("Most Requested Technical Skills")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("skill_demand.png", dpi=150)
plt.close()

connection.close()

print("Charts created successfully")