import logging
from pathlib import Path

LOG_FOLDER = Path('log/')

def setup_logging():
    root = logging.getLogger()

    if root.handlers:
        return

    root.setLevel(logging.DEBUG)

    handler = logging.FileHandler(LOG_FOLDER / 'movie_manager.log', encoding='utf-8')
    handler.setFormatter(
        logging.Formatter(
            # fmt = '{asctime} [{levelname}] {filename} | {message}',
            fmt = '{asctime} [{levelname}] {name} | {message}',
            datefmt = '%Y-%m-%d %H:%M:%S',
            style   = '{'
        )
    )
    root.addHandler(handler)