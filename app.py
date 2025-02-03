import pandas as pd
import streamlit as st
from dbhelper import DB
import visuals

db = DB()

st.set_page_config(
    page_title="PSL",  # Optional, customize the page title
    page_icon="🌟",              # Optional, add a custom icon
    layout="wide"                # Set layout to wide
)

# Dashboard Header
st.title("PSL Performance Dashboard")

# Sidebar Options
st.sidebar.title("PSL Analytics")

main_menu = st.sidebar.selectbox("Main Menu", ["Batting Performance", "Bowling Performance", "Recommended Players"])

if main_menu == 'Batting Performance':
    option = st.sidebar.selectbox("Select options", ["Overall", "Players"])

    if option == "Overall":
        # Fetch season data
        data = db.fetch_season()

        # Sidebar Filters
        st.sidebar.subheader("Filters")
        season = st.sidebar.selectbox("Select Season", data)
        top_players = st.sidebar.radio("Metric", ["Top 10 Runs", "Top 10 Average Batting", "Top 10 Strike Rate",
                                                  "Top 10 Boundaries Hit"])

        # Fetch players' performance
        df = db.fetch_players_record(season)

        # Data sorted by total_runs (top 10 players by runs)
        df1 = df.head(10)

        # Top Batting average of those players who played atleast 5 matches
        df2 = df[df['Matches Played'] >= 5].sort_values(by='Batting Average', ascending=False).head(10)

        # Top Strike of those players who faced atleast 60 balls
        df3 = df[df['Balls faced'] >= 60].sort_values(by='Strike rate', ascending=False).head(10)

        # Top 10 Players who hit the most boundries
        df4 = df.sort_values(by='Boundaries hit', ascending=False).head(10)

        if top_players == 'Top 10 Runs':
            visuals.Batting_performance(df1)
        elif top_players == 'Top 10 Average Batting':
            visuals.Batting_performance(df2)
        elif top_players == 'Top 10 Strike Rate':
            visuals.Batting_performance(df3)
        else:
            visuals.Batting_performance(df4)


    else:

        # Fetch season data
        names = db.fetch_names()

        # Sidebar Filters
        st.sidebar.subheader("Filters")

        # Sidebar for filter player
        name = st.sidebar.selectbox("Select Player", names)

        seasons = db.player_season(name)
        # Sidebar for filter season
        season = st.sidebar.selectbox("Select Season", seasons)

        # df = db.fetch_players_record(season)

        # record = df[df['Batsman'] == name]

        if name == "choose a player":
            st.sidebar.write("Please select a player to see the details.")
        else:
            visuals.individual_performance(season, name)

else:
    pass
    # option = st.sidebar.selectbox("Select options", ["Overall", "Players"])
    #
    # if option == "Overall":
    #     # Fetch season data
    #     data = db.fetch_season()
    #
    #     # Sidebar Filters
    #     st.sidebar.subheader("Filters")
    #     season = st.sidebar.selectbox("Select Season", data)
    #     top_players = st.sidebar.radio("Metric", ["Top 10 Runs", "Top 10 Average Batting", "Top 10 Strike Rate",
    #                                               "Top 10 Boundaries Hit"])
    #
    #     # Fetch players' performance
    #     df = db.fetch_players_record(season)
    #
    #     # Data sorted by total_runs (top 10 players by runs)
    #     df1 = df.head(10)
    #
    #     # Top Batting average of those players who played atleast 5 matches
    #     df2 = df[df['Matches Played'] >= 5].sort_values(by='Batting Average', ascending=False).head(10)
    #
    #     # Top Strike of those players who faced atleast 60 balls
    #     df3 = df[df['Balls faced'] >= 60].sort_values(by='Strike rate', ascending=False).head(10)
    #
    #     # Top 10 Players who hit the most boundries
    #     df4 = df.sort_values(by='Boundaries hit', ascending=False).head(10)
    #
    #     if top_players == 'Top 10 Runs':
    #         visuals.Batting_performance(df1)
    #     elif top_players == 'Top 10 Average Batting':
    #         visuals.Batting_performance(df2)
    #     elif top_players == 'Top 10 Strike Rate':
    #         visuals.Batting_performance(df3)
    #     else:
    #         visuals.Batting_performance(df4)
    #
    #
    # else:
    #     # Fetch season data
    #     names = db.fetch_names()
    #
    #     # Sidebar Filters
    #     st.sidebar.subheader("Filters")
    #
    #     # Sidebar for filter player
    #     name = st.sidebar.selectbox("Select Player", names)
    #
    #     seasons = db.player_season(name)
    #     # Sidebar for filter season
    #     season = st.sidebar.selectbox("Select Season", seasons)
    #
    #     # df = db.fetch_players_record(season)
    #
    #     # record = df[df['Batsman'] == name]
    #
    #     if name == "choose a player":
    #         st.sidebar.write("Please select a player to see the details.")
    #     else:
    #         visuals.individual_performance(season, name)

