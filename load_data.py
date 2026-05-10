"""Load cleaned CSV files into a compliant SQLite database.

Creates `working/patents_standard.db` using the schema in `schema.sql` (assignment field names).

Usage:
    python3 load_data.py
"""
import sqlite3
import pandas as pd
from pathlib import Path

WORKING = Path('working')
DB_PATH = WORKING / 'patents_standard.db'

def create_schema(conn):
    sql = Path('schema.sql').read_text()
    conn.executescript(sql)

def load_table_from_csv(conn, table, df, dtype_map=None):
    df.to_sql(table, conn, if_exists='append', index=False)

def main():
    if not WORKING.exists():
        raise SystemExit('working/ directory not found')

    conn = sqlite3.connect(str(DB_PATH))
    # create schema
    create_schema(conn)

    # Load patents, map columns to assignment names
    patents_csv = WORKING / 'clean_patents.csv'
    if patents_csv.exists():
        patents = pd.read_csv(patents_csv)
        # map existing names to required names
        rename_map = {}
        if 'patent_title' in patents.columns:
            rename_map['patent_title'] = 'title'
        if 'patent_abstract' in patents.columns:
            rename_map['patent_abstract'] = 'abstract'
        if 'patent_date' in patents.columns:
            rename_map['patent_date'] = 'filing_date'
        patents = patents.rename(columns=rename_map)
        # ensure expected columns exist
        expected = ['patent_id', 'title', 'abstract', 'filing_date', 'year']
        for c in expected:
            if c not in patents.columns:
                patents[c] = None
        patents = patents[expected]
        load_table_from_csv(conn, 'patents', patents)

    # inventors
    inventors_csv = WORKING / 'clean_inventors.csv'
    if inventors_csv.exists():
        inventors = pd.read_csv(inventors_csv)
        # ensure columns
        for c in ['inventor_id', 'name', 'country']:
            if c not in inventors.columns:
                inventors[c] = None
        inventors = inventors[['inventor_id', 'name', 'country']]
        load_table_from_csv(conn, 'inventors', inventors)

    # companies
    companies_csv = WORKING / 'clean_companies.csv'
    if companies_csv.exists():
        companies = pd.read_csv(companies_csv)
        for c in ['company_id', 'name']:
            if c not in companies.columns:
                companies[c] = None
        companies = companies[['company_id', 'name']]
        load_table_from_csv(conn, 'companies', companies)

    # relationships
    rel_csv = WORKING / 'relationships.csv'
    if rel_csv.exists():
        rel = pd.read_csv(rel_csv)
        for c in ['patent_id', 'inventor_id', 'company_id']:
            if c not in rel.columns:
                rel[c] = None
        rel = rel[['patent_id', 'inventor_id', 'company_id']]
        load_table_from_csv(conn, 'relationships', rel)

    conn.commit()
    conn.close()
    print('Database written to', DB_PATH)

if __name__ == '__main__':
    main()
