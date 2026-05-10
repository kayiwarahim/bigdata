#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"/..
echo "1) Cleaning data (if needed)"
python3 scripts/clean_data.py
echo "2) Build DB"
python3 scripts/build_db.py
echo "3) Generate reports"
python3 scripts/generate_reports.py
echo "Done."
