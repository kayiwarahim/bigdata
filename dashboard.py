import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# -----------------------------------
# CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Patent Intelligence Dashboard",
    layout="wide"
)

DB_PATH = "working/patents.db"


# -----------------------------------
# DB CONNECTION
# -----------------------------------
@st.cache_data
def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# -----------------------------------
# TITLE
# -----------------------------------
st.title("Global Patent Intelligence Dashboard")

st.markdown("Analyze patents, inventors, companies, and trends.")

# -----------------------------------
# KPI METRICS
# -----------------------------------
col1, col2, col3 = st.columns(3)

total_patents = run_query("SELECT COUNT(*) as total FROM patents")['total'][0]
total_inventors = run_query("SELECT COUNT(*) as total FROM inventors")['total'][0]
total_companies = run_query("SELECT COUNT(*) as total FROM companies")['total'][0]

col1.metric("Total Patents", f"{total_patents:,}")
col2.metric("Total Inventors", f"{total_inventors:,}")
col3.metric("Total Companies", f"{total_companies:,}")

st.divider()

# -----------------------------------
# TOP INVENTORS
# -----------------------------------
st.subheader("Top Inventors")

top_inventors = run_query("""
SELECT i.name, COUNT(*) AS total_patents
FROM relationships r
JOIN inventors i ON r.inventor_id = i.inventor_id
GROUP BY i.name
ORDER BY total_patents DESC
LIMIT 10
""")

st.dataframe(top_inventors, use_container_width=True)

# -----------------------------------
# TOP COMPANIES
# -----------------------------------
st.subheader("Top Companies")

top_companies = run_query("""
SELECT c.name, COUNT(*) AS total_patents
FROM relationships r
JOIN companies c ON r.company_id = c.company_id
GROUP BY c.name
ORDER BY total_patents DESC
LIMIT 10
""")

st.dataframe(top_companies, use_container_width=True)

# -----------------------------------
# TOP COUNTRIES
# -----------------------------------
st.subheader("Top Countries")

top_countries = run_query("""
SELECT country, COUNT(*) AS total
FROM inventors
GROUP BY country
ORDER BY total DESC
LIMIT 10
""")

st.bar_chart(top_countries.set_index('country'))

# -----------------------------------
# TRENDS OVER TIME
# -----------------------------------
st.subheader("Patent Trends Over Time")

trends = run_query("""
SELECT year, COUNT(*) AS total_patents
FROM patents
WHERE year > 0
GROUP BY year
ORDER BY year
""")

fig, ax = plt.subplots()
ax.plot(trends['year'], trends['total_patents'])
ax.set_title("Patents per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Count")

st.pyplot(fig)

# -----------------------------------
# SEARCH SECTION
# -----------------------------------
st.subheader("Search Patents")

search_term = st.text_input("Enter keyword (title search):")

if search_term:
    results = run_query(f"""
    SELECT patent_title, year
    FROM patents
    WHERE patent_title LIKE '%{search_term}%'
    LIMIT 50
    """)
    
    st.write(f"Results for '{search_term}':")
    st.dataframe(results, use_container_width=True)

# -----------------------------------
# JOIN DATA VIEW
# -----------------------------------
st.subheader("Sample Patent Relationships")

joined_data = run_query("""
SELECT p.patent_title, i.name AS inventor, c.name AS company
FROM relationships r
JOIN patents p ON r.patent_id = p.patent_id
JOIN inventors i ON r.inventor_id = i.inventor_id
JOIN companies c ON r.company_id = c.company_id
LIMIT 50
""")

st.dataframe(joined_data, use_container_width=True)

# -----------------------------------
# FOOTER
# -----------------------------------
st.divider()
st.caption("Built with Streamlit | Patent Data Pipeline Project")