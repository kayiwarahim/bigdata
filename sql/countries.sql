-- Q3: Countries — which countries produce the most patents (by inventor country)
SELECT country, COUNT(*) AS total
FROM inventors i
JOIN relationships r ON i.inventor_id = r.inventor_id
GROUP BY country
ORDER BY total DESC
LIMIT 20;
