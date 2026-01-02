import streamlit as st
import pandas as pd
from pathlib import Path
from utils.streamlit_helpers import df_statistics
from utils.sql import list_sql_files
from utils.db import get_connection

st.set_page_config(page_title = 'SQL', page_icon='🔮', layout='wide')

tab_predefined, tab_custom = st.tabs(['📄 Predefined SQL', '✍️ Custom SQL'])

with tab_predefined:
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

with tab_custom:
    st.warning('Only SELECT queries are allowed. Changes to the database are blocked.')

    sql_input = st.text_area(
        label='Write SQL query',
        height=200,
        placeholder='SELECT * FROM movie_detail LIMIT 10;'
    ).strip()

    if st.button('Run SQL', type='primary'):
        if not sql_input:
            st.warning('Please enter a SQL query.')
            st.stop()

        dangerous = (' insert ', ' update ', ' delete ', ' drop ', ' alter ')
        if any(word in sql_input.lower() for word in dangerous):
            st.error('Only SELECT queries are allowed.')
            st.stop()

        with get_connection() as con:
            try:
                from time import perf_counter
                start = perf_counter()
                df = pd.read_sql_query(sql_input, con)
                st.success(f"Query executed in {(perf_counter() - start):.3f} seconds.")
                st.dataframe(df, hide_index=True, width='content')
                st.write(df_statistics(df))
            except Exception as e:
                st.exception(e)
                st.stop()
