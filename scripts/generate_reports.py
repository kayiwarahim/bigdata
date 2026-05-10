"""Run the SQL files under `sql/` against `working/patents_standard.db` and write outputs to working/.

Usage:
    python3 scripts/generate_reports.py
"""
import sqlite3
import pandas as pd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'working' / 'patents_standard.db'
SQL_DIR = ROOT / 'sql'
OUT = ROOT / 'working'

def run_sql_file(conn, path):
    sql = path.read_text()
    return pd.read_sql_query(sql, conn)

def main():
    if not DB.exists():
        raise SystemExit(f'Database not found: {DB} — run build_db first')
    conn = sqlite3.connect(str(DB))
    outputs = {}
    # Map some sql files to output names
    mapping = {
        'Q1_top_inventors.sql':'top_inventors.csv',
        'Q2_top_companies.sql':'top_companies.csv',
        'Q3_countries.sql':'country_trends.csv',
        'Q4_trends_over_time.sql':'trends_over_time.csv',
    }
    for sql_file in sorted(SQL_DIR.glob('*.sql')):
        try:
            df = run_sql_file(conn, sql_file)
            name = mapping.get(sql_file.name, sql_file.stem + '.csv')
            outp = OUT / name
            df.to_csv(outp, index=False)
            outputs[sql_file.name] = df.head(10).to_dict(orient='records')
            print('Wrote', outp)
        except Exception as e:
            print('Failed to run', sql_file.name, e)

    # Write a small JSON report summarizing top results
    report_path = OUT / 'report_from_sql.json'
    with open(report_path, 'w') as f:
        json.dump(outputs, f, indent=2)
    print('Wrote', report_path)
    conn.close()

if __name__ == '__main__':
    main()
