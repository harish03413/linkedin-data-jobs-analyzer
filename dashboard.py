import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Jobs Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("Jobs Analyzer")
st.write("Upload a CSV file to explore job titles, locations, companies, salary, and technical skill demand.")

st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload a job dataset",
    type=["csv"],
    key="job_csv_uploader"
)

if uploaded_file is None:
    st.info("Please upload a CSV file to view the dashboard.")
    st.stop()

uploaded_file.seek(0)
st.success(f"Loaded file: {uploaded_file.name}")

try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error("Could not read the CSV file. Please upload a valid CSV.")
    st.exception(e)
    st.stop()

df.columns = df.columns.astype(str)
source_name = st.sidebar.text_input("Enter source name", value="Other")
df["source"] = source_name

def find_first_col(frame, keywords):
    cols = [c for c in frame.columns if any(k in c.lower() for k in keywords)]
    return cols[0] if cols else None

title_col = find_first_col(df, ["title", "role", "position", "job_title"])
company_col = find_first_col(df, ["company", "employer", "organization", "firm"])
location_col = find_first_col(df, ["location", "loc", "city", "country", "remote"])
salary_col = find_first_col(df, ["salary", "compensation", "pay", "wage", "estimate"])

skill_columns = {
    "SQL": ["skill_sql", "sql"],
    "Python": ["skill_python", "python"],
    "Excel": ["skill_excel", "excel"],
    "Power BI": ["skill_power_bi", "power_bi", "power bi"],
    "Tableau": ["skill_tableau", "tableau"],
    "AWS": ["skill_aws", "aws"],
    "Azure": ["skill_azure", "azure"],
    "Snowflake": ["skill_snowflake", "snowflake"],
    "Databricks": ["skill_databricks", "databricks"],
    "BigQuery": ["skill_bigquery", "bigquery"],
    "dbt": ["skill_dbt", "dbt"],
    "Airflow": ["skill_airflow", "airflow"],
    "Looker": ["skill_looker", "looker"],
    "Spark": ["skill_spark", "spark"],
    "ETL": ["skill_etl", "etl"],
    "Statistics": ["skill_statistics", "statistics"],
    "Communication": ["skill_communication", "communication"],
    "Data Visualization": ["skill_data_visualization", "data visualization"],
    "Data Analysis": ["skill_data_analysis", "data analysis"],
    "Machine Learning": ["skill_machine_learning", "machine_learning", "machine learning"]
}

def get_count_series(frame, key_words):
    col = find_first_col(frame, key_words)
    if col is None:
        return None, None
    s = frame[col]
    if s.dtype == bool:
        return col, int(s.fillna(False).sum())
    if pd.api.types.is_numeric_dtype(s):
        return col, int((s.fillna(0) > 0).sum())
    normalized = s.astype(str).str.strip().str.lower()
    truthy = normalized.isin(["true", "1", "yes", "y", "present"]) | normalized.notna()
    return col, int(truthy.sum())

if not any([title_col, company_col, location_col, salary_col]):
    st.error("No usable title/company/location/salary columns were found in this file.")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

st.sidebar.header("Filters")
location_filter_values = ["All locations"]
if location_col:
    location_values = sorted(df[location_col].dropna().astype(str).unique().tolist())
    location_filter_values.extend(location_values)

selected_location = st.sidebar.selectbox("Select location", location_filter_values)
filtered_df = df.copy()

if selected_location != "All locations" and location_col:
    filtered_df = filtered_df[filtered_df[location_col].astype(str) == selected_location]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total postings", len(filtered_df))
with c2:
    st.metric("Companies", filtered_df[company_col].nunique() if company_col else 0)
with c3:
    st.metric("Locations", filtered_df[location_col].nunique() if location_col else 0)
with c4:
    st.metric("Salary columns", 1 if salary_col else 0)

st.subheader("Detected Columns")
col_map = pd.DataFrame({
    "field": ["title", "company", "location", "salary"],
    "matched_column": [title_col, company_col, location_col, salary_col]
})
st.dataframe(col_map, width="stretch", hide_index=True)

st.subheader("Salary Details")
if salary_col:
    st.write("Matched salary column:", salary_col)
    st.dataframe(filtered_df[[salary_col]].head(20), width="stretch", hide_index=True)
else:
    st.info("No salary-related column found.")

st.subheader("Top Job Titles")
if title_col:
    title_counts = (
        filtered_df[title_col]
        .dropna()
        .astype(str)
        .value_counts()
        .head(10)
        .rename_axis("title")
        .reset_index(name="job_count")
    )
    if not title_counts.empty:
        st.bar_chart(title_counts, x="title", y="job_count", horizontal=True)
    else:
        st.info("No job titles found in the filtered data.")
else:
    st.info("No title-related column found.")

st.subheader("Top Hiring Companies")
if company_col:
    company_counts = (
        filtered_df[company_col]
        .dropna()
        .astype(str)
        .value_counts()
        .head(10)
        .rename_axis("company")
        .reset_index(name="job_count")
    )
    if not company_counts.empty:
        st.bar_chart(company_counts, x="company", y="job_count", horizontal=True)
    else:
        st.info("No company names found in the filtered data.")
else:
    st.info("No company-related column found.")

st.subheader("Location Details")
if location_col:
    st.dataframe(filtered_df[[location_col]].head(20), width="stretch", hide_index=True)
else:
    st.info("No location-related column found.")

st.subheader("Technical Skill Demand")
skill_results = []

for skill_name, keywords in skill_columns.items():
    col, count = get_count_series(filtered_df, keywords)
    if col is not None:
        skill_results.append({"skill": skill_name, "job_count": int(count), "matched_column": col})

skill_df = pd.DataFrame(skill_results)

if not skill_df.empty:
    skill_df = skill_df.sort_values("job_count", ascending=False)
    st.bar_chart(skill_df, x="skill", y="job_count")
    st.dataframe(skill_df, width="stretch", hide_index=True)
else:
    st.info("No skill columns are available in this dataset.")

st.subheader("Filtered Data")
show_cols = [c for c in [title_col, company_col, location_col, salary_col, "source"] if c]
if show_cols:
    st.dataframe(filtered_df[show_cols].head(100), width="stretch", hide_index=True)
else:
    st.dataframe(filtered_df.head(100), width="stretch", hide_index=True)