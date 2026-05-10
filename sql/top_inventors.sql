-- Q1: Top Inventors — who has the most patents
SELECT i.inventor_id, i.name, COUNT(*) AS total_patents
FROM relationships r
JOIN inventors i ON r.inventor_id = i.inventor_id
GROUP BY i.inventor_id, i.name
ORDER BY total_patents DESC
LIMIT 20;
