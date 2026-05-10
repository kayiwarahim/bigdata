-- Q2: Top Companies — which companies own the most patents
SELECT c.company_id, c.name, COUNT(*) AS total_patents
FROM relationships r
JOIN companies c ON r.company_id = c.company_id
GROUP BY c.company_id, c.name
ORDER BY total_patents DESC
LIMIT 20;
