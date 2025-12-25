-- List recently watched
SELECT * FROM (
    SELECT * FROM movie_detail 
    WHERE status in ('completed', 'dropped')
    ORDER BY watched_date DESC 
    LIMIT (?)
) 
ORDER BY watched_date;