-- Q4: Trends Over Time — patents created per year
SELECT year, COUNT(*) AS total_patents
FROM patents
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year;
