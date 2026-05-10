"""Build the compliant SQLite DB by invoking the existing `load_data.py`.

Usage:
    python3 scripts/build_db.py
"""
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parent.parent
LOADER = ROOT / 'load_data.py'
DB = ROOT / 'working' / 'patents_standard.db'

def main():
    if not LOADER.exists():
        raise SystemExit('load_data.py not found at ' + str(LOADER))
    # remove existing DB to ensure clean create
    if DB.exists():
        print('Removing existing DB at', DB)
        DB.unlink()
    proc = subprocess.run([sys.executable, str(LOADER)], capture_output=True, text=True)
    print(proc.stdout)
    if proc.returncode != 0:
        print('Loader failed:', proc.stderr)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
