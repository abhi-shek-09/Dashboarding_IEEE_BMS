import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    initial_sidebar_state='expanded',
    page_title='Business Dashboard',
    page_icon='📈',
    layout='wide')


def market_size(major_market, small_market):
    labels = ['Major Market', 'Small Market']
    colors = ['yellow', 'orange']
    values = [major_market, small_market]
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors),
        textinfo='none',
        hoverinfo='label+percent',
        showlegend=True,
    )])
    fig.update_layout(
        autosize=False,
        width=400,
        height=400,
        margin=dict(l=10, r=10, t=0, b=20),
        annotations=[
            dict(
                text=f'Major vs Small Markets',
                x=0.5,
                y=0.5,
                font=dict(size=16, color="black"),
                showarrow=False,
            )
        ]
    )
    return fig


df = pd.read_csv('Final_Dataset.csv')
tab1, tab2 = st.tabs(['Operations Analysis', 'Product Analysis'])
with tab1:
    col1, col2, col3 = st.columns([5, 1, 5])
    with col1:
        heatmap_data = df.pivot_table(index='State', values='Sales', aggfunc='sum').fillna(0)
        st.title('Sales Heatmap Across States')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='.2f', ax=ax)
        st.pyplot(fig)

    with col2:
        pass

    with col3:
        major_markets, small_markets = df['Market_size'].value_counts().values
        st.markdown(f"Major Markets: {major_markets}, Small Markets: {small_markets}")
        st.plotly_chart(market_size(major_market=major_markets, small_market=small_markets))


    col1, col2, col3 = st.columns([5, 1, 5])
    with col1:
        time_column = 'Date'
        category_column = 'Product_type'
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Formatted_Date'] = df['Date'].dt.strftime('%m/%d/%Y')
        df[time_column] = pd.to_datetime(df[time_column])
        fig = px.area(df, x=time_column, y=df[category_column], color=category_column, title=f'Stacked Area Chart of {category_column} Over Time')
        st.plotly_chart(fig)
    

with tab2:
    product_counts = df.groupby(['Product_line', 'Product_type', 'Product', 'Type']).size().reset_index(name='Count')
    st.write("## Product Counts by Category")
    st.table(product_counts)
    st.write("## Product Type Distribution")
    product_type_distribution = df['Product_type'].value_counts()
    col1, col2, col3 = st.columns([5, 1, 5])
    with col1:
        st.bar_chart(product_type_distribution)
    with col2:
        pass
    with col3:
        market_size_column = 'Market_size'
        product_type_column = 'Product_type'
        fig = px.bar(df, x=market_size_column, color=product_type_column, title=f'Distribution of Product Types in Major and Small Markets')
        st.plotly_chart(fig)