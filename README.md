# Big Data Patent Pipeline

This project builds a lightweight data pipeline over USPTO patent TSV files. It loads large files in chunks, normalizes key entities (patents, inventors, companies), and produces cleaned CSV outputs plus a small SQLite database for analysis.

## Project layout

- `big-data.ipynb`: End-to-end pipeline notebook.
- `g_*` folders: Source TSV datasets.
- `working/`: Generated outputs (cleaned CSVs, reports, and SQLite database).

## What the pipeline does

1. Reads large TSV files with chunked loading.
2. Cleans and normalizes:
   - patents (title, date, abstract, year)
   - inventors (name + country)
   - companies (assignee names)
   - relationships (patent–inventor–company)
3. Writes cleaned CSVs to `working/`.
4. Builds a SQLite database at `working/patents.db`.
5. Produces summary reports (top inventors, top companies, country trends) and a JSON report.

## Inputs

The notebook expects the following datasets under the project root:

- `g_patent/g_patent.tsv`
- `g_patent_abstract/g_patent_abstract.tsv`
- `g_inventor_disambiguated/g_inventor_disambiguated.tsv`
- `g_persistent_inventor/g_persistent_inventor.tsv`
- `g_assignee_disambiguated/g_assignee_disambiguated.tsv`
- `g_persistent_assignee/g_persistent_assignee.tsv`
- `g_location_disambiguated/g_location_disambiguated.tsv`

## Outputs (written to `working/`)

- `clean_patents.csv`
- `clean_inventors.csv`
- `clean_companies.csv`
- `relationships.csv`
- `patents.db`
- `top_inventors.csv`
- `top_companies.csv`
- `country_trends.csv`
- `report.json`

## Running the notebook

Open `big-data.ipynb` and run cells in order. The notebook prints progress messages as it loads data, cleans tables, builds the SQLite database, and generates reports.

## Notes

- The loader uses chunked reads to handle large TSV files efficiently.
- Update file paths in the notebook if you move datasets to another location.
