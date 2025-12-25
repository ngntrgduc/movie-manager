import streamlit as st

pg = st.navigation(
    [
        st.Page("pages/1_data.py", title="Data"),  # number before name for ordering purpose
        st.Page("pages/2_add_movie.py", title="Add"),
        st.Page("pages/3_edit_movie.py", title="Edit"),
        st.Page("pages/4_visualization.py", title="Visualization"),
        st.Page("pages/5_sql.py", title="SQL"),
        st.Page("pages/6_backup_restore.py", title="Backup & Restore"),
    ],
    position="top"
)
pg.run()