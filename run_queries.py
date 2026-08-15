import duckdb

connection = duckdb.connect("job_postings.duckdb")


def run_query(title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    results = connection.execute(query).fetchdf()
    print(results)


run_query(
    "TOP JOB TITLES",
    """
    SELECT
        title,
        COUNT(*) AS job_count
    FROM job_postings
    WHERE title IS NOT NULL
    GROUP BY title
    ORDER BY job_count DESC
    LIMIT 10
    """
)


run_query(
    "TOP COMPANIES",
    """
    SELECT
        company,
        COUNT(*) AS job_count
    FROM job_postings
    WHERE company IS NOT NULL
    GROUP BY company
    ORDER BY job_count DESC
    LIMIT 10
    """
)


run_query(
    "TOP LOCATIONS",
    """
    SELECT
        location,
        COUNT(*) AS job_count
    FROM job_postings
    WHERE location IS NOT NULL
    GROUP BY location
    ORDER BY job_count DESC
    LIMIT 10
    """
)


run_query(
    "OVERALL SKILL DEMAND",
    """
    SELECT
        SUM(CAST(skill_sql AS INTEGER)) AS sql_jobs,
        SUM(CAST(skill_python AS INTEGER)) AS python_jobs,
        SUM(CAST(skill_excel AS INTEGER)) AS excel_jobs,
        SUM(CAST(skill_power_bi AS INTEGER)) AS power_bi_jobs,
        SUM(CAST(skill_tableau AS INTEGER)) AS tableau_jobs,
        SUM(CAST(skill_aws AS INTEGER)) AS aws_jobs,
        SUM(CAST(skill_machine_learning AS INTEGER)) AS machine_learning_jobs
    FROM job_postings
    """
)


run_query(
    "SKILLS IN DATA ANALYST JOBS",
    """
    SELECT
        SUM(CAST(skill_sql AS INTEGER)) AS sql_jobs,
        SUM(CAST(skill_python AS INTEGER)) AS python_jobs,
        SUM(CAST(skill_excel AS INTEGER)) AS excel_jobs,
        SUM(CAST(skill_power_bi AS INTEGER)) AS power_bi_jobs,
        SUM(CAST(skill_tableau AS INTEGER)) AS tableau_jobs,
        SUM(CAST(skill_aws AS INTEGER)) AS aws_jobs,
        SUM(CAST(skill_machine_learning AS INTEGER)) AS machine_learning_jobs
    FROM job_postings
    WHERE LOWER(title) LIKE '%data analyst%'
    """
)


run_query(
    "POSTINGS BY DATE",
    """
    SELECT
        CAST(date_posted AS DATE) AS posted_date,
        COUNT(*) AS job_count
    FROM job_postings
    WHERE date_posted IS NOT NULL
    GROUP BY posted_date
    ORDER BY posted_date
    """
)


connection.close()