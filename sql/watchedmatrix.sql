SELECT
    SUBSTR(watched_date_normalized, 1, 4) AS watch_year
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '01' AND date_precision != 'year' THEN 1 ELSE 0 END) AS jan
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '02' AND date_precision != 'year' THEN 1 ELSE 0 END) AS feb
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '03' AND date_precision != 'year' THEN 1 ELSE 0 END) AS mar
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '04' AND date_precision != 'year' THEN 1 ELSE 0 END) AS apr
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '05' AND date_precision != 'year' THEN 1 ELSE 0 END) AS may
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '06' AND date_precision != 'year' THEN 1 ELSE 0 END) AS jun
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '07' AND date_precision != 'year' THEN 1 ELSE 0 END) AS jul
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '08' AND date_precision != 'year' THEN 1 ELSE 0 END) AS aug
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '09' AND date_precision != 'year' THEN 1 ELSE 0 END) AS sep
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '10' AND date_precision != 'year' THEN 1 ELSE 0 END) AS oct
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '11' AND date_precision != 'year' THEN 1 ELSE 0 END) AS nov
    , SUM(CASE WHEN SUBSTR(watched_date_normalized, 6, 2) = '12' AND date_precision != 'year' THEN 1 ELSE 0 END) AS dec
    , COUNT(*) AS total
FROM (
    SELECT
        CASE
            WHEN LENGTH(watched_date) = 4 THEN watched_date || '-01-01'
            WHEN LENGTH(watched_date) = 7 THEN watched_date || '-01'
            ELSE watched_date
        END AS watched_date_normalized
        , CASE
            WHEN LENGTH(watched_date) = 4 THEN 'year'
            WHEN LENGTH(watched_date) = 7 THEN 'month'
            ELSE 'day'
        END AS date_precision
        , rating
    FROM movie
    WHERE status = 'completed'
)
GROUP BY watch_year
ORDER BY watch_year

--WITH RECURSIVE normalized_movies AS (
--    SELECT
--        *
--        , CASE
--            WHEN LENGTH(watched_date) = 4 THEN watched_date || '-01-01'
--            WHEN LENGTH(watched_date) = 7 THEN watched_date || '-01'
--            ELSE watched_date
--          END AS watched_date_normalized
--    FROM movie
--    WHERE status = 'completed'
--),
--completed_by_month AS (
--    SELECT
--        SUBSTR(watched_date_normalized, 1, 4) AS watch_year
--        , SUBSTR(watched_date_normalized, 6, 2) AS watch_month
--        , rating
--    FROM normalized_movies
--),
--month_spine(spine_date) AS (
--    SELECT MIN(watched_date_normalized) FROM normalized_movies
--    UNION ALL
--    SELECT date(spine_date, '+1 month')
--    FROM month_spine
--    WHERE spine_date < (SELECT MAX(watched_date_normalized) FROM normalized_movies)
--),
--year_spine AS (
--    SELECT DISTINCT SUBSTR(spine_date, 1, 4) AS watch_year
--    FROM month_spine
--)
--SELECT
--    ys.watch_year
--    , SUM(CASE WHEN cbm.watch_month = '01' THEN 1 ELSE 0 END) AS jan
--    , SUM(CASE WHEN cbm.watch_month = '02' THEN 1 ELSE 0 END) AS feb
--    , SUM(CASE WHEN cbm.watch_month = '03' THEN 1 ELSE 0 END) AS mar
--    , SUM(CASE WHEN cbm.watch_month = '04' THEN 1 ELSE 0 END) AS apr
--    , SUM(CASE WHEN cbm.watch_month = '05' THEN 1 ELSE 0 END) AS may
--    , SUM(CASE WHEN cbm.watch_month = '06' THEN 1 ELSE 0 END) AS jun
--    , SUM(CASE WHEN cbm.watch_month = '07' THEN 1 ELSE 0 END) AS jul
--    , SUM(CASE WHEN cbm.watch_month = '08' THEN 1 ELSE 0 END) AS aug
--    , SUM(CASE WHEN cbm.watch_month = '09' THEN 1 ELSE 0 END) AS sep
--    , SUM(CASE WHEN cbm.watch_month = '10' THEN 1 ELSE 0 END) AS oct
--    , SUM(CASE WHEN cbm.watch_month = '11' THEN 1 ELSE 0 END) AS nov
--    , SUM(CASE WHEN cbm.watch_month = '12' THEN 1 ELSE 0 END) AS dec
--    , COUNT(*) as count
--FROM year_spine AS ys
--LEFT JOIN completed_by_month AS cbm
--    ON cbm.watch_year = ys.watch_year
--GROUP BY ys.watch_year
--ORDER BY ys.watch_year