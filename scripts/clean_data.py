"""Clean raw PatentsView TSVs into the expected cleaned CSVs.

This script prefers existing `working/*.csv` files and will skip work if they exist.
If raw `g_*` folders exist, it will attempt to read TSV files and create cleaned outputs.

Usage:
    python3 scripts/clean_data.py
"""
from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parent.parent
WORKING = ROOT / 'working'
WORKING.mkdir(exist_ok=True)

def file_exists_check():
    expected = ['clean_patents.csv','clean_inventors.csv','clean_companies.csv','relationships.csv']
    return all((WORKING / f).exists() for f in expected)

def try_load_tsv(path, usecols=None):
    if not path.exists():
        return None
    try:
        return pd.read_csv(path, sep='\t', dtype=str, usecols=usecols)
    except Exception:
        return pd.read_csv(path, sep='\t', dtype=str)

def main():
    if file_exists_check():
        print('Cleaned CSVs already exist in working/. Skipping cleaning.')
        return

    # Attempt to read pre-cleaned files if present
    # Otherwise, try raw g_* TSVs listed in README
    g_patent = ROOT / 'g_patent' / 'g_patent.tsv'
    g_abstract = ROOT / 'g_patent_abstract' / 'g_patent_abstract.tsv'
    g_inventor = ROOT / 'g_inventor_disambiguated' / 'g_inventor_disambiguated.tsv'
    g_assignee = ROOT / 'g_assignee_disambiguated' / 'g_assignee_disambiguated.tsv'

    # Patents
    patents = try_load_tsv(g_patent)
    if patents is None:
        print('No raw patent TSV found at', g_patent)
    else:
        # minimal selection / renaming
        cols = {}
        if 'patent_id' in patents.columns:
            cols['patent_id'] = 'patent_id'
        if 'patent_title' in patents.columns:
            patents = patents.rename(columns={'patent_title':'title'})
        if 'patent_date' in patents.columns:
            patents = patents.rename(columns={'patent_date':'filing_date'})
        # ensure columns exist
        patents['title'] = patents.get('title')
        patents['abstract'] = None
        if g_abstract.exists():
            abs_df = try_load_tsv(g_abstract)
            if abs_df is not None and 'patent_id' in abs_df.columns and 'patent_abstract' in abs_df.columns:
                patents = patents.merge(abs_df[['patent_id','patent_abstract']], on='patent_id', how='left')
                patents = patents.rename(columns={'patent_abstract':'abstract'})
        patents['year'] = pd.to_datetime(patents.get('filing_date'), errors='coerce').dt.year
        patents = patents.rename(columns={'title':'title','abstract':'abstract','filing_date':'filing_date','year':'year'})
        outp = WORKING / 'clean_patents.csv'
        patents[['patent_id','title','abstract','filing_date','year']].to_csv(outp, index=False)
        print('Wrote', outp)

    # Inventors
    inventors = try_load_tsv(g_inventor)
    if inventors is None:
        print('No raw inventor TSV found at', g_inventor)
    else:
        # minimal normalization
        if 'inventor_id' not in inventors.columns and 'id' in inventors.columns:
            inventors = inventors.rename(columns={'id':'inventor_id'})
        if 'name' not in inventors.columns and 'inventor_name' in inventors.columns:
            inventors = inventors.rename(columns={'inventor_name':'name'})
        inventors_out = WORKING / 'clean_inventors.csv'
        inventors[['inventor_id','name','country']].to_csv(inventors_out, index=False)
        print('Wrote', inventors_out)

    # Companies / assignees
    assignees = try_load_tsv(g_assignee)
    if assignees is None:
        print('No raw assignee TSV found at', g_assignee)
    else:
        if 'assignee_id' in assignees.columns:
            assignees = assignees.rename(columns={'assignee_id':'company_id'})
        if 'assignee_organization' in assignees.columns:
            assignees = assignees.rename(columns={'assignee_organization':'name'})
        companies_out = WORKING / 'clean_companies.csv'
        assignees[['company_id','name']].drop_duplicates().to_csv(companies_out, index=False)
        print('Wrote', companies_out)

    # Relationships: try to build from patent-inventor mappings if present
    rel_out = WORKING / 'relationships.csv'
    # if relationships already present from other processing, skip
    if (WORKING / 'relationships.csv').exists():
        print('relationships.csv exists; skipping relation assembly')
    else:
        # try to create from persistent records if present
        # This is a best-effort; if absent, we'll leave relationships missing
        print('No relationships assembled (raw mapping not found).')

if __name__ == '__main__':
    main()
