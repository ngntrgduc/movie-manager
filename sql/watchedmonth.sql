-- statistics for watched over months
SELECT 
	watched_month
	, COUNT(*) AS count
	, ROUND(AVG(rating),2) AS avg_rating 
FROM (
	SELECT *, SUBSTR(watched_date, 1, 7) AS watched_month
	FROM movie_detail md
	WHERE status = 'completed'
)
GROUP BY watched_month
ORDER BY watched_month ASC