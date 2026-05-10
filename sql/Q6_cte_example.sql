-- Q6: CTE example — inventor counts with threshold
WITH inventor_counts AS (
    SELECT inventor_id, COUNT(*) AS total
    FROM relationships
    GROUP BY inventor_id
)
SELECT ic.inventor_id, i.name, ic.total
FROM inventor_counts ic
LEFT JOIN inventors i ON ic.inventor_id = i.inventor_id
WHERE ic.total > 5
ORDER BY ic.total DESC;
