-- Standard schema matching assignment field names
CREATE TABLE patents (
    patent_id INTEGER PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    filing_date TEXT,
    year INTEGER
);

CREATE TABLE inventors (
    inventor_id TEXT PRIMARY KEY,
    name TEXT,
    country TEXT
);

CREATE TABLE companies (
    company_id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE relationships (
    patent_id INTEGER,
    inventor_id TEXT,
    company_id TEXT
);