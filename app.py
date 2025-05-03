import streamlit as st
from dbhelper import DB
import visuals

db = DB()

st.set_page_config(
    page_title="PSL",  # Optional, customize the page title
    page_icon="🥎",              # Optional, add a custom icon
    layout="wide"                # Set layout to wide
)

# Dashboard Header
st.title("PSL Performance Dashboard")

# Sidebar Options
st.sidebar.title("PSL Analytics")

main_menu = st.sidebar.selectbox("Main Menu", ["Batting Performance", "Bowling Performance"])

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

        # Fetch players' record
        df = db.batters_df(season)

        # Data sorted by total_runs (top 10 players by runs)
        df1 = df.head(10)

        # Top Batting average of those players who played atleast 5 matches
        df2 = df[df['Matches Played'] >= 5].sort_values(by='Batting Average', ascending=False).head(10)

        # Top Strike of those players who faced atleast 60 balls
        df3 = df[df['Balls faced'] >= 60].sort_values(by='Strike rate', ascending=False).head(10)

        # Top 10 Players who hit the most boundries
        df4 = df.sort_values(by='Boundaries hit', ascending=False).head(10)

        if top_players == 'Top 10 Runs':
            visuals.overall_batting(df1, top_players)
        elif top_players == 'Top 10 Average Batting':
            visuals.overall_batting(df2, top_players)
        elif top_players == 'Top 10 Strike Rate':
            visuals.overall_batting(df3, top_players)
        else:
            visuals.overall_batting(df4, top_players)


    else:

        # Fetch season data
        names = db.fetch_batters_names()

        # Sidebar Filters
        st.sidebar.subheader("Filters")

        # Sidebar for filter player
        name = st.sidebar.selectbox("Select Player", names)

        seasons = db.batters_season(name)
        # Sidebar for filter season
        season = st.sidebar.selectbox("Select Season", seasons)

        if name == "choose a player":
            st.write("Please select a player to see the details.")
        else:
            visuals.batter_performance(season, name)


elif main_menu == 'Bowling Performance':
    option = st.sidebar.selectbox("Select options", ["Overall", "Players"])

    if option == "Overall":
        # Fetch season data
        data = db.fetch_season()

        # Sidebar Filters
        st.sidebar.subheader("Filters")
        season = st.sidebar.selectbox("Select Season", data)

        top_playersz = st.sidebar.radio("Metric", ["Top Wickets", "Best Average Bowling", "Best Economy Rate",
                                                  "Best Strike Rate (Bowling)"])

        # Fetch players' record
        df = db.bowling_stats(season)

        # Data sorted by total wickets (top 10 players by wickets)
        df1 = df.head(10)


        df2 = df[df['Total Wickets'] >= 10].sort_values(by='Bowling Average', ascending=True).head(10)


        df3 = df[df['Total Wickets'] >= 10].sort_values(by='Economy Rate', ascending=True).head(10)


        df4 = df[df['Total Wickets'] >= 10].sort_values(by='Strike Rate', ascending=True).head(10)

        if top_players == 'Top Wickets':
            visuals.overall_bowling(df1,top_players)
        elif top_players == 'Best Average Bowling':
            visuals.overall_bowling(df2, top_players)
        elif top_players == 'Best Economy Rate':
            visuals.overall_bowling(df3,top_players)
        else:
            visuals.overall_bowling(df4, top_players)

    else:
        # Fetch season data
        names = db.fetch_bowlers_names()

        # Sidebar Filters
        st.sidebar.subheader("Filters")

        # Sidebar for filter player
        name = st.sidebar.selectbox("Select Player", names)

        seasons = db.bowlers_season(name)
        # Sidebar for filter season
        season = st.sidebar.selectbox("Select Season", seasons)

        if name == "choose a player":
            st.write("Please select a player to see the details.")
        else:
            visuals.bowler_performance(season, name)