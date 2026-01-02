SELECT * FROM (
    SELECT * FROM movie_detail
    WHERE status = 'waiting'
    ORDER BY id DESC
    LIMIT 5
)
ORDER BY id ASC