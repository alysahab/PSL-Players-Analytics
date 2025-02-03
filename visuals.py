import streamlit as st
import plotly.express as px
from dbhelper import DB

db = DB()

# for overall
def Batting_performance(data):
    # KPI Metrics
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Highest Runs", int(data["Runs scored"].max()))
    col2.metric("Highest Strike Rate", f"{data['Strike rate'].max():.2f}")
    col3.metric("Highest Average", f"{data['Batting Average'].max():.2f}")
    col4.metric("Most Boundaries", data["Boundaries hit"].max())

    # Tabs for Visualizations
    st.markdown("---")
    tab1, tab2 = st.tabs(["Charts", "Details"])

    with tab1:
        # Side-by-side charts
        st.subheader("Performance Visualizations")
        col1, col2 = st.columns(2)

        with col1:
            fig_runs = px.bar(
                data,
                y="Batsman",
                x="Runs scored",
                text_auto=True,
                color="Runs scored",
                title="Runs by players",
                color_continuous_scale="Blues"
            )
            fig_runs.update_layout(
                xaxis_title="Runs scored",
                yaxis_title="",
                yaxis=dict(categoryorder="total ascending")
            )
            st.plotly_chart(fig_runs)

        with col2:
            fig_strike = px.scatter(
                data,
                y="Strike rate",
                x="Batsman",
                color="Strike rate",
                size="Strike rate",
                title="Strike Rate",
                color_continuous_scale="Viridis",
            )
            fig_strike.update_layout(
                xaxis_title="",
                yaxis_title="Strike Rate",
                xaxis_tickangle=-90

            )
            st.plotly_chart(fig_strike)

        col3, col4 = st.columns(2)
        with col3:
            fig_avg = px.bar(
                data,
                y="Batsman",
                x="Batting Average",
                text_auto=True,
                color="Batting Average",
                title="Batting Averages by players",
                color_continuous_scale="Oranges"
            )
            fig_avg.update_layout(
                xaxis_title="Batting Average",
                yaxis_title="",
                yaxis=dict(categoryorder="total ascending")
            )
            st.plotly_chart(fig_avg)

        with col4:
            fig_boundaries = px.scatter(
                data,
                y="Boundaries hit",
                x="Batsman",
                color="Boundaries hit",
                size="Boundaries hit",
                title="Boundaries Hit",
                color_continuous_scale="Reds",
            )
            fig_boundaries.update_layout(
                xaxis_title="",
                yaxis_title="Boundaries Hit",
                xaxis_tickangle=-90
            )
            st.plotly_chart(fig_boundaries)

    with tab2:
        # Dataframe for details
        st.subheader("Player Details")
        st.dataframe(data)



# For players option
def individual_performance(season, name):
    metric = db.fetch_individual_overall(season, name)
    try:
        # KPI Metrics
        st.markdown("### Key Performance Indicators")
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        col1.metric("Matches", round(metric["Match Played"]))
        col2.metric("Runs", metric['Runs'].astype(int))
        col3.metric("Strike rate", metric['Strike Rate'])
        col4.metric("Average Batting", metric['Batting Average'])
        col5.metric("Fours", metric["fours"].astype(int))
        col6.metric("Sixes", metric["sixes"].astype(int))
        col7.metric("50s", round(metric["50s"]))
        col8.metric("100s", round(metric["100s"]))
    except:
        st.write(metric)

    # Tabs for Visualizations
    st.markdown("---")
    tab1, tab2 = st.tabs(["Charts", "Details"])

    with tab1:
        # Side-by-side charts
        st.subheader("Player Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.write('Player detail')
            overview = db.fetch_player_overview(name)
            overview = overview.drop(columns='Player')
            overview = overview.melt(var_name='overview', value_name='details')
            st.dataframe(overview)
        with col2:
            st.write('Team')
            team = db.fetch_player_team(season,name)
            st.dataframe(team)

        if season == 'All Season':
            individual_record = db.fetch_individual_record(name)
            if individual_record.Season.nunique() > 1:
                fig_runs = px.line(
                    individual_record,
                    x="Season",
                    y="Runs scored",
                    title="Runs by season",
                    markers= 'o'
                )
                fig_runs.update_layout(
                    yaxis_title="Runs scored",
                    xaxis_title="Season",
                    yaxis=dict(categoryorder="total ascending")
                )
                st.plotly_chart(fig_runs)


        col3,col4 = st.columns([2,3])
        with col3:
            run_against_team = db.run_against_team(season,name)
            fig_runs = px.bar(
                run_against_team,
                x="opponent_team",
                y="runs",
                title="Runs against team",
                color_continuous_scale= 'Viridis',
                text_auto=True
            )
            fig_runs.update_layout(
                xaxis_title="opponent Team",
                yaxis_title="Runs",
                yaxis=dict(categoryorder="total ascending"),
                height = 600
            )
            st.plotly_chart(fig_runs, use_container_width=True)

        with col4:
            dismissal = db.player_dismissal(season, name)
            fig1_runs = px.scatter(
                dismissal,
                x = 'dismissed_by',
                y = 'wickets',
                title='Most Dismissal by Bowlers',
                color_continuous_scale='Virdis'
            )
            fig1_runs.update_layout(
                xaxis_title="Bowler",
                yaxis_title="Wickets",
                yaxis=dict(categoryorder="total ascending"),
                height=300
            )
            st.plotly_chart(fig1_runs, use_container_width=True)

            wicket_type = db.player_wicket_type(season, name)
            fig2_runs = px.pie(
                wicket_type,
                values='wickets',
                color = 'wicket_type',
                title="Wicket Type",
                names='wicket_type'
            )
            fig2_runs.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                height = 300
            )
            st.plotly_chart(fig2_runs, use_container_width=True)

    with tab2:
        # Dataframe for details
        individual_record = db.fetch_individual_record(name)
        individual_record.Season = individual_record.Season.astype(str)
        st.subheader("Player Details")
        st.dataframe(individual_record)
