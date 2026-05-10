-- Q7: Ranking query — rank inventors using window functions
SELECT inventor_id, name, total, RANK() OVER (ORDER BY total DESC) AS rank
FROM (
    SELECT i.inventor_id, i.name, COUNT(*) AS total
    FROM relationships r
    JOIN inventors i ON r.inventor_id = i.inventor_id
    GROUP BY i.inventor_id, i.name
) sub
ORDER BY rank
LIMIT 100;
