"""Modern Streamlit dashboard for patent intelligence analytics."""

import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Patent Intelligence Dashboard",
    page_icon=".",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "working/patents.db"

# -----------------------------------
# CUSTOM CSS (MODERN UI)
# -----------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1e293b 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1, h2, h3 {
    color: white !important;
}

.metric-card {
    background: linear-gradient(135deg, #1e293b, #111827);
    padding: 24px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
}

.metric-title {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 500;
}

.metric-value {
    color: white;
    font-size: 36px;
    font-weight: 700;
    margin-top: 8px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

div[data-testid="stDataFrame"] {
    background: #111827;
    border-radius: 18px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.08);
}

.stTextInput input {
    background-color: #111827;
    color: white;
    border-radius: 12px;
    border: 1px solid #334155;
    padding: 12px;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# DB CONNECTION
# -----------------------------------
@st.cache_data
def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)

# -----------------------------------
# SIDEBAR
# -----------------------------------
with st.sidebar:
    st.title(" Patent Intel")
    st.markdown("### Navigation")

    section = st.radio(
        "Go to",
        [
            "Overview",
            "Inventors",
            "Companies",
            "Countries",
            "Search",
            "Relationships"
        ]
    )


# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("""
<h1 style='font-size:48px;'> Global Patent Intelligence</h1>
<p style='color:#94a3b8; font-size:18px;'>
Analyze patents, inventors, companies, and innovation trends worldwide.
</p>
""", unsafe_allow_html=True)

# -----------------------------------
# KPI METRICS
# -----------------------------------
total_patents = run_query(
    "SELECT COUNT(*) AS total FROM patents"
)["total"][0]

total_inventors = run_query(
    "SELECT COUNT(*) AS total FROM inventors"
)["total"][0]

total_companies = run_query(
    "SELECT COUNT(*) AS total FROM companies"
)["total"][0]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL PATENTS</div>
        <div class="metric-value">{total_patents:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL INVENTORS</div>
        <div class="metric-value">{total_inventors:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL COMPANIES</div>
        <div class="metric-value">{total_companies:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===================================
# OVERVIEW
# ===================================
if section == "Overview":

    col1, col2 = st.columns([1, 1])

    # -----------------------------------
    # TRENDS OVER TIME
    # -----------------------------------
    trends = run_query("""
    SELECT year, COUNT(*) AS total_patents
    FROM patents
    WHERE year > 0
    GROUP BY year
    ORDER BY year
    """)

    fig = px.line(
        trends,
        x="year",
        y="total_patents",
        markers=True,
        template="plotly_dark",
        title="Patent Trends Over Time"
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        height=450,
        xaxis_title="Year",
        yaxis_title="Patent Count"
    )

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------
    # TOP COUNTRIES
    # -----------------------------------
    top_countries = run_query("""
    SELECT country, COUNT(*) AS total
    FROM inventors
    GROUP BY country
    ORDER BY total DESC
    LIMIT 10
    """)

    fig2 = px.bar(
        top_countries,
        x="country",
        y="total",
        template="plotly_dark",
        title="Top Countries by Inventors"
    )

    fig2.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        height=450
    )

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

# ===================================
# INVENTORS
# ===================================
elif section == "Inventors":

    st.subheader(" Top Inventors")

    top_inventors = run_query("""
    SELECT i.name, COUNT(*) AS total_patents
    FROM relationships r
    JOIN inventors i ON r.inventor_id = i.inventor_id
    GROUP BY i.name
    ORDER BY total_patents DESC
    LIMIT 20
    """)

    fig = px.bar(
        top_inventors,
        x="total_patents",
        y="name",
        orientation="h",
        template="plotly_dark",
        title="Leading Inventors"
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        height=700,
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_inventors, use_container_width=True)

# ===================================
# COMPANIES
# ===================================
elif section == "Companies":

    st.subheader("Top Companies")

    top_companies = run_query("""
    SELECT c.name, COUNT(*) AS total_patents
    FROM relationships r
    JOIN companies c ON r.company_id = c.company_id
    GROUP BY c.name
    ORDER BY total_patents DESC
    LIMIT 20
    """)

    fig = px.pie(
        top_companies,
        names="name",
        values="total_patents",
        template="plotly_dark",
        title="Patent Distribution by Company"
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top_companies, use_container_width=True)

# ===================================
# COUNTRIES
# ===================================
elif section == "Countries":

    st.subheader("Country Analytics")

    top_countries = run_query("""
    SELECT country, COUNT(*) AS total
    FROM inventors
    GROUP BY country
    ORDER BY total DESC
    LIMIT 25
    """)

    fig = px.choropleth(
        top_countries,
        locations="country",
        locationmode="country names",
        color="total",
        template="plotly_dark",
        title="Global Innovation Distribution"
    )

    fig.update_layout(
        paper_bgcolor="#111827",
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

# ===================================
# SEARCH
# ===================================
elif section == "Search":

    st.subheader("Search Patents")

    search_term = st.text_input(
        "Enter keyword to search patent titles"
    )

    if search_term:

        results = run_query("""
        SELECT patent_title, year
        FROM patents
        WHERE patent_title LIKE ?
        LIMIT 50
        """, (f"%{search_term}%",))

        st.success(f"Found {len(results)} results")

        st.dataframe(
            results,
            use_container_width=True,
            height=600
        )

# ===================================
# RELATIONSHIPS
# ===================================
elif section == "Relationships":

    st.subheader("Patent Relationships")

    joined_data = run_query("""
    SELECT
        p.patent_title,
        i.name AS inventor,
        c.name AS company
    FROM relationships r
    JOIN patents p ON r.patent_id = p.patent_id
    JOIN inventors i ON r.inventor_id = i.inventor_id
    JOIN companies c ON r.company_id = c.company_id
    LIMIT 100
    """)

    st.dataframe(
        joined_data,
        use_container_width=True,
        height=700
    )

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.caption(" Patent Intelligence Analytics Dashboard ")