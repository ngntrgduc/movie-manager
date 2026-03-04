SELECT * FROM movie_detail
WHERE status = 'waiting'
ORDER BY RANDOM()
LIMIT 5