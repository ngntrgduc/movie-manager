import streamlit as st

from utils.streamlit_helpers import load_data_with_cache

st.set_page_config(page_title = 'Visualization', page_icon='🎨', layout='wide')

def watched_df(df):
    return df.where((df['status'] == 'completed') | (df['status'] == 'dropped'))

def group_df(df, columns: list[str]):
    return df.groupby(columns).size().reset_index(name='count')

df = load_data_with_cache()
df['watched_date'] = df['watched_date'].apply(lambda d: d[:4] if d else '')

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader('Watched by year')
    st.bar_chart(
        group_df(watched_df(df), ['watched_date', 'type']),
        x='watched_date',
        y='count',
        color='type',
        x_label='year'
        # horizontal=True,
    )

with col2:
    st.subheader('Rating distribution')
    st.bar_chart(
        group_df(df, ['rating', 'type']),
        x='rating',
        y='count',
        color='type',
        horizontal=True,
        stack=True,
        sort='-rating',
    )

with col3:
    st.subheader('Status distribution')
    st.bar_chart(
        group_df(df, ['status', 'type']),
        x='status',
        y='count',
        color='type',
        # color='status',
        horizontal=True,
        stack=False
    )

col1, col2 = st.columns(2)
with col1:
    st.subheader('Country by status')
    st.bar_chart(
        group_df(df, ['country', 'status']),
        x='country',
        y='count',
        color='status',
        horizontal=True,
        stack='normalize',
    )
    
with col2:
    st.subheader('Type by status')
    st.bar_chart(
        group_df(df, ['type', 'status']),
        x='type',
        y='count',
        color='status',
        horizontal=True,
        # stack='normalize',
    )
    

# Year distribution
# year_df = df.groupby(["year", "type"]).size().reset_index(name="count")
# st.subheader("Movies & Series by Year")
# st.bar_chart(
#     year_df,
#     x="year",
#     y="count",
#     color="type",
# )