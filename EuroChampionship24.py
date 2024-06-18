import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
st.set_page_config(layout="wide")

title_html = """
    <style>
        .title {
            font-family: 'Arial', sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: #333333; /* You can use any color code you like */
            text-align: center;
            padding: 0px;
        }
    </style>
    <h1 class="title">LaC UEFA Euro 2024 Championship!</h1>
"""

df = pd.read_csv('Res_2.csv')
#df.index = df.Date
#
df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
df.index = df['Date']
#df.drop(columns='Date', inplace=True)
#st.write(df)

start_date = datetime(2024, 6, 13)
end_date = datetime(2024, 6, 26)


latest_scores = df[df['Date'] == df.iloc[-1,0]].iloc[0, 1:-1]
#st.write(latest_scores)

top_users_df = latest_scores.sort_values(ascending=False)

with st.sidebar:
    st.write('Latest results:')
    st.table(top_users_df.astype("str"))

top_users = top_users_df.index

users_per_plot = 8#5, 13, 5]
user_groups = user_groups = [top_users[:5], top_users[5:10], top_users[10:15], top_users[15:]]#[top_users[i:i + users_per_plot] for i in range(0, len(top_users), users_per_plot)]

#st-write()

#st.write()
st.markdown(title_html, unsafe_allow_html=True)

titles = ['The Master Scorer Squad!', 'The Upper Median Masters!', 'The Mid-Range Mavericks!','The Last-Minute Legends!']

for igroups, users in enumerate(user_groups):
    
    fig = go.Figure()

    for user in users:
        #st.line_chart(df.iloc[-1])
        #fig = px.line(df, x="Date", y=users)



        # Add scatter plot with markers on top of the line plot
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[user],
            mode='lines+markers',  # Show both lines and markers
            name=user,
            line_shape='linear',
            #title="layout.hovermode='x'",
            line=dict(width=1),  # Customize line color and width
            #hoveron={'info': True},
            marker=dict(symbol='circle', size=6, line=dict(width=0.5)),  # Circle markers
            hoverinfo='text',  # Use text for hover info
            text=df.apply(lambda row: f"Group {row['info']}, {user},{row[user]}", axis=1)  # Custom hover info
        ))

    #fig.update_layout(hovermode='x')
    fig.update_traces(mode="markers+lines", hovertemplate=None)#'%{text}<extra></extra>')

    fig.update_layout(
        xaxis=dict(
            range=[start_date, end_date],
            title='Date'
        ),
        yaxis=dict(title='Scores'),
        height=300,
        #width = 1300,
        
        margin=dict(l=10, r=10, t=15, b=15),
        paper_bgcolor='rgba(0,0,0,0)',  # Make the plot background transparent
        plot_bgcolor='rgba(0,0,0,0)',   # Make the plot background transparent
        title={
            'text': titles[igroups],
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top'
        }
    )
    st.markdown("""---""")
    st.plotly_chart(fig, use_container_width=True)
    
