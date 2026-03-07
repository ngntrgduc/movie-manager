-- List oldest waiting movie
SELECT * FROM movie_detail
WHERE status = 'waiting'
    AND year < 2000
ORDER BY year ASC
-- LIMIT 10