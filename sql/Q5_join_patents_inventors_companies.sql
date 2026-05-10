-- Q5: JOIN Query — combine patents with inventors and companies
SELECT p.patent_id, p.title, p.filing_date, i.inventor_id, i.name AS inventor_name, c.company_id, c.name AS company_name
FROM relationships r
JOIN patents p ON r.patent_id = p.patent_id
LEFT JOIN inventors i ON r.inventor_id = i.inventor_id
LEFT JOIN companies c ON r.company_id = c.company_id
LIMIT 100;
