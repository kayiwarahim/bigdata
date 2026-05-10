CREATE TABLE "companies" (
"company_id" TEXT,
  "name" TEXT
);

CREATE TABLE "inventors" (
"inventor_id" TEXT,
  "name" TEXT,
  "country" TEXT
);

CREATE TABLE "patents" (
"patent_id" INTEGER,
  "patent_date" TEXT,
  "patent_title" TEXT,
  "patent_abstract" TEXT,
  "year" INTEGER
);

CREATE TABLE "relationships" (
"patent_id" TEXT,
"inventor_id" TEXT,
  "company_id" TEXT
);