import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(
    page_title="LinkedIn Data Jobs Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("LinkedIn Data Jobs Analyzer")
st.write(
    "Explore job titles, locations, companies, and technical skill demand."
)

@st.cache_resource
def get_connection():
    return duckdb.connect("job_postings.duckdb", read_only=True)

@st.cache_data
def load_data():
    connection = get_connection()
    return connection.execute(
        "SELECT * FROM job_postings"
    ).fetchdf()

df = load_data()

st.sidebar.header("Filters")

locations = sorted(
    df["location"].dropna().astype(str).unique().tolist()
)

selected_location = st.sidebar.selectbox(
    "Select location",
    ["All locations"] + locations
)

filtered_df = df.copy()

if selected_location != "All locations":
    filtered_df = filtered_df[
        filtered_df["location"].astype(str) == selected_location
    ]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total postings", len(filtered_df))

with col2:
    st.metric(
        "Companies",
        filtered_df["company"].nunique()
    )

with col3:
    st.metric(
        "Locations",
        filtered_df["location"].nunique()
    )

st.subheader("Top Job Titles")

title_counts = (
    filtered_df["title"]
    .value_counts()
    .head(10)
    .rename_axis("title")
    .reset_index(name="job_count")
)

st.bar_chart(
    title_counts,
    x="title",
    y="job_count",
    horizontal=True
)

st.subheader("Top Hiring Companies")

company_counts = (
    filtered_df["company"]
    .value_counts()
    .head(10)
    .rename_axis("company")
    .reset_index(name="job_count")
)

st.bar_chart(
    company_counts,
    x="company",
    y="job_count",
    horizontal=True
)

st.subheader("Technical Skill Demand")

skill_columns = {
    "SQL": "skill_sql",
    "Python": "skill_python",
    "Excel": "skill_excel",
    "Power BI": "skill_power_bi",
    "Tableau": "skill_tableau",
    "AWS": "skill_aws",
    "Machine Learning": "skill_machine_learning"
}

skill_results = []

for skill_name, column_name in skill_columns.items():
    if column_name in filtered_df.columns:
        count = filtered_df[column_name].fillna(0).astype(int).sum()
        skill_results.append({
            "skill": skill_name,
            "job_count": count
        })

skill_df = pd.DataFrame(skill_results)
skill_df = skill_df.sort_values("job_count", ascending=False)

st.bar_chart(
    skill_df,
    x="skill",
    y="job_count"
)

st.subheader("Filtered Data")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)