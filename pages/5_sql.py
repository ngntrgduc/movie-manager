import streamlit as st
import pandas as pd
from pathlib import Path
from utils.streamlit_helpers import df_statistics
from utils.sql import list_sql_files
from utils.db import get_connection

st.set_page_config(page_title = 'SQL', page_icon='🔮', layout='wide')

sql_folder = Path('sql/')

sql_file = st.selectbox(
    label='SQL scripts', 
    options=list_sql_files(sql_folder), 
    index=None, 
    width=300
)

if sql_file:
    sql_code = (sql_folder / sql_file).with_suffix('.sql').read_text()
    with st.expander('See SQL code', width='stretch', expanded=True):
        st.code(sql_code, language='sql')

    with get_connection() as con:
        df = pd.read_sql_query(sql_code, con)
        st.dataframe(df, hide_index=True, width='content')
        st.write(df_statistics(df))