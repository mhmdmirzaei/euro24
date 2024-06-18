import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

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

start_date = datetime(2024, 6, 14)
end_date = datetime(2024, 6, 26)


latest_scores = df[df['Date'] == df.iloc[-1,0]].iloc[0, 1:]
top_users = latest_scores.sort_values(ascending=False).index

users_per_plot = 8#5, 13, 5]
user_groups = user_groups = [top_users[:5], top_users[5:10], top_users[10:15], top_users[15:]]#[top_users[i:i + users_per_plot] for i in range(0, len(top_users), users_per_plot)]

#st-write()

#st.write()
st.markdown(title_html, unsafe_allow_html=True)

titles = ['The Master Scorer Squad!', 'The Upper Median Masters!', 'The Mid-Range Mavericks!','The Last-Minute Legends!']

for igroups, users in enumerate(user_groups):
    #st.line_chart(df.iloc[-1])
    fig = px.line(df, x="Date", y=users)

    fig.update_layout(
        xaxis=dict(
            range=[start_date, end_date],
            title='Date'
        ),
        yaxis=dict(title='Scores'),
        height=300,
        width = 900,
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
    st.plotly_chart(fig)#, use_container_width=True)
    