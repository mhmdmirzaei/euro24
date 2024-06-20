import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os
import csv


from datetime import datetime
st.set_page_config(layout="wide")

# Define the CSV file name
csv_file = 'visits.csv'



def add_date(df):
    #st.write(df)


    return df


@st.cache_data
def load_data():
    df = pd.read_csv('Res_2.csv')

    df.rename(columns={'Unnamed: 0':'Date'}, inplace=True)
    df.index = df['Date']

    dfu = pd.read_pickle('dfs_pickle.pkl')
    dfu['Date'] = dfu.index

    #st.write(df)

    return df, dfu




def plot_them_all(df, user_groups, titles):

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

df, dfs = load_data()
# Create tabs
tab1, tab2 = st.tabs(["Results", "Scenarios"])

# Content for Tab 1
with tab1:

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

    st.markdown(
        """
        <style>
        body {
            background-image: url('./uefa.jpg');
            background-size: cover;
            background-attachment: fixed;
        }
        .css-1v3fvcr {
            background: rgba(0, 0, 0, 0);  /* Transparent background for Streamlit main container */
        }
        </style>
        """+title_html,
        unsafe_allow_html=True
    )

    
    #df.index = df.Date
    #

    #df.drop(columns='Date', inplace=True)
    #st.write(df)

    start_date = datetime(2024, 6, 14)
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
    #st.markdown(title_html, unsafe_allow_html=True)

    titles = ['The Master Scorer Squad!', 'The Upper Median Masters!', 'The Mid-Range Mavericks!','The Last-Minute Legends!']
        
    plot_them_all(df, user_groups, titles)

    # Function to get the current timestamp
    def get_current_timestamp():
        return datetime.now()

    # Initialize or load the visits CSV
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["timestamp"])
        df.to_csv(csv_file, index=False)

    # Record the visit
    now = get_current_timestamp()
    new_visit = pd.DataFrame([[now]], columns=["timestamp"])
    new_visit.to_csv(csv_file, mode='a', header=False, index=False)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

# Content for Tab 2
with tab2:
    user_v = st.selectbox(
    "Select a user to run the scenario of 'What happens if that user gets it right from now on!'?",
    tuple(dfs.columns.levels[0][:-1]), index=None, placeholder="Select...")
    
    #st.write(type(user_v))

    if user_v==None:
        st.write('it is none!')
    else:
        st.write('it is not none!')

        dfu = dfs[user_v]

        dfu['Date'] = dfu.index

        #st.write(dfu)

        latest_scores = dfu.iloc[-1].iloc[0:-2]#dfu[dfu['Date'] == dfu.iloc[-1,0]].iloc[0, 1:-1]
        #st.write(latest_scores)

        top_users_df = latest_scores.sort_values(ascending=False)

        top_users = top_users_df.index

        users_per_plot = 8#5, 13, 5]
        user_groups = user_groups = [top_users[:5], top_users[5:10], top_users[10:15], top_users[15:]]#[top_users[i:i + users_per_plot] for i in range(0, len(top_users), users_per_plot)]        

        plot_them_all(dfu, user_groups, titles)
   
