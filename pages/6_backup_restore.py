import streamlit as st
from pathlib import Path
import sqlite3
from utils.db import get_connection
from utils.movie import load_movies

st.set_page_config(page_title = 'Backup & Restore', page_icon='💽', layout='centered')

DB_FILE = Path('data/movies.db')
BACKUP_FILE = Path('data/backup.db')

def update_csv() -> None:
    """Update CSV file with data from database."""
    with get_connection() as con:
        df = load_movies(con, with_index=True)
        df.to_csv('data/data.csv', index=False)

def backup() -> None:
    try:
        with sqlite3.connect(BACKUP_FILE) as backup_con:
            with get_connection() as db_con:
                db_con.backup(backup_con)

        st.toast(f'Backup successful.', icon='✅')
    except Exception as e:
        st.exception(e)

def restore() -> None:
    if not BACKUP_FILE.exists():
        st.toast("**Backup file not found. Run 'Back up' first.**", icon='❌')
        return

    import shutil
    try:
        shutil.copyfile(BACKUP_FILE, DB_FILE)
        update_csv()
        st.toast(f'Restore successful.', icon='✅')
    except Exception as e:
        st.exception(e)

from utils.file import get_last_modified
@st.dialog('Are you sure?')
def run(operation) -> None:
    st.write(f'Backup last modified: `{get_last_modified(BACKUP_FILE)}`')
    if operation == 'backup':
        st.write('This will overwrite the existing backup file. Continue?')
        if st.button('Yes', type='primary'):
            backup()

    if operation == 'restore':
        st.write('This will replace your current movie database with the backup file. Continue?')
        if st.button('Yes', type='primary'):
            restore()

col1, col2 = st.columns(2)
with col1:
    st.text_input('Database file', value=DB_FILE, disabled=True)
with col2:
    st.text_input('Backup file', value=BACKUP_FILE, disabled=True)

with st.container(horizontal=True, horizontal_alignment='distribute'):
    if st.button('Back up', type='primary'):
        run('backup')
    if st.button('Restore', type='primary'):
        run('restore')
