from pathlib import Path
import re

INFO_PREFIX = re.compile(r'\[INFO\].*?\|')
ID_BLOCK = re.compile(r'\s+id=\d.*?:')
ADDED_TYPE = re.compile(r'Added\s+(movie|series)')

def clean_log(line: str) -> str:
    """Remove unnecessary info from a log line"""
    line = INFO_PREFIX.sub('|', line)
    line = ID_BLOCK.sub(':', line)  # remove id
    line = ADDED_TYPE.sub(lambda x: f'{x.group(1):<6}', line)  # align colon
    return line

LOG_FOLDER = Path('log/')
log_file = LOG_FOLDER / 'movie_manager.log'
with open(LOG_FOLDER / 'info_add.log', 'w') as f:
    for line in log_file.read_text().splitlines():
        if '[INFO]' in line and 'Added' in line:
            f.write(f'{clean_log(line)}\n')