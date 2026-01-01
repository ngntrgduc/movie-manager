import sqlite3
import pandas as pd
from utils.movie import add_movie
import logging

logger = logging.getLogger('csv_to_sqlite')

def csv_to_sqlite(df: pd.DataFrame, con: sqlite3.Connection) -> None:
    """Export csv data to SQLite database."""
    cur = con.cursor()

    # Temporarily silence INFO logs from utils.movie for bulk adding
    movie_logger = logging.getLogger('utils.movie')
    previous_level = movie_logger.level
    movie_logger.setLevel(logging.WARNING)

    try:
        df['genres'] = df['genres'].fillna('').str.split(',')
        for _, movie in df.iterrows():
            movie_dict = dict(movie)
            # Convert pandas NaN to None for SQLite
            # When reading CSV with pandas, numeric columns with missing values become NaN.
            # SQLite does not understand NaN, so we convert them to None which maps to NULL in SQLite.
            movie_dict['year'] = int(movie['year']) if not pd.isna(movie['year']) else None
            movie_dict['rating'] = float(movie['rating']) if not pd.isna(movie['rating']) else None
            add_movie(movie_dict, cur)
    finally:
        movie_logger.setLevel(previous_level)

if __name__ == '__main__':
    from time import perf_counter
    from pathlib import Path
    from logging_config import setup_logging

    setup_logging()

    tic = perf_counter()
    DB_PATH = Path('data/movies.db')
    CSV_PATH = Path('data/data.csv')

    if DB_PATH.exists():
        print(f'Database file {DB_PATH} still exists, deleting...')
        try:
            DB_PATH.unlink()
            print(f'Deleted database file. Re-creating it with data from {CSV_PATH}...')
        except PermissionError:
            print('Cannot delete database: it is open in another program. Close it first.')
            raise SystemExit

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    with open('sql/schema.sql', 'r') as f:
        schema_sql = f.read()

    cur.executescript(schema_sql)
    con.commit()

    df = pd.read_csv(CSV_PATH)
    csv_to_sqlite(df, con)
    con.commit()

    con.close()
    duration = perf_counter() - tic
    print(f'Moved data from CSV to SQLite database, took {duration:.4f}s.')
    logger.info('Imported %s movies from CSV file=%s, took %.4f', len(df), CSV_PATH, duration)
