import streamlit as st
import plotly.express as px
from dbhelper import DB

db = DB()

# for overall
def overall_batting(data, option):
    # KPI Metrics
    if option == 'Top 10 Runs':
        st.markdown("### Top 10 Run Scorers – Stats")
    elif option == 'Top 10 Average Batting':
        st.markdown("### Top 10 Batting Averages – Stats")
    elif option == 'Top 10 Strike Rate':
        st.markdown("### Top 10 Strike Rates – Stats")
    else:
        st.markdown("### Top 10 Boundary Hitters – Stats")

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
def batter_performance(season, name):
    metric = db.batter_metrics(season, name)
    try:
        # KPI Metrics
        st.markdown("### Key Performance Indicators")
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

        col1.metric("Matches", round(metric["Match Played"]))
        col2.metric("Runs", metric['Runs'].astype(int))
        col3.metric("Strike Rate", metric['Strike Rate'])
        col4.metric("Batting Average", metric['Batting Average'])
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
            team = db.fetch_player_team(season,name, 'batter')
            st.dataframe(team)

        if season == 'All Season':
            batters_record = db.individual_batter_record(name)
            if batters_record.Season.nunique() > 1:
                fig_runs = px.line(
                    batters_record,
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
        batters_record = db.individual_batter_record(name)
        batters_record.Season = batters_record.Season.astype(str)
        st.subheader("Player Details")
        st.dataframe(batters_record)

def overall_bowling(data, option):
    # KPI Metrics
    if option == 'Top 10 Wickets':
        st.markdown("### Top 10 Wickets Taker – Stats")
    elif option == 'Top 10 Average Bowling':
        st.markdown("### Average Bowling – Stats")
    elif option == 'Top 10 Strike Rate (Bowling)':
        st.markdown("### Top 10 Strike Rates – Stats")
    else:
        st.markdown("### Top 10 Economy - Stats")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Max Wickets", int(data["Total Wickets"].max()))
    col2.metric("Best Strike Rate", f"{data['Strike Rate'].min():.2f}")
    col3.metric("Best Average bowling", f"{data['Bowling Average'].min():.2f}")
    col4.metric("Best Economy Rate", data["Economy Rate"].min())

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
                y="Bowler",
                x="Total Wickets",
                text_auto=True,
                title="Total Wickets",
                color = 'Total Wickets',
                color_continuous_scale="Blues"
            )
            fig_runs.update_layout(
                xaxis_title="Wickets Taken",
                yaxis_title="",
                yaxis=dict(categoryorder="total ascending")
            )
            st.plotly_chart(fig_runs)

        with col2:
            fig = px.scatter(
                data,
                x="Bowler",
                y="Bowling Average",
                size="Strike Rate",
                color="Strike Rate",
                title="Bowling Average and Strike Rate (Lower is Better)",
                color_continuous_scale="Viridis",
            )
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Bowling Average",
                xaxis_tickangle=-90
            )
            st.plotly_chart(fig)


        col3, col4 = st.columns(2)
        with col3:
            df = data[['Bowler','Total Balls','Dot Ball Percent', 'Boundary Ball Percent','Non-Boundary Ball Percent']].melt(id_vars=['Bowler','Total Balls'],
                                                                                                                  var_name='Metric',
                                                                                                                  value_name='Percentage')

            fig_avg = px.bar(
                df,
                x="Total Balls",  # Changed to "Percentage" for scaling
                y="Bowler",
                color="Metric",
                title="Bowling Performance Breakdown",
                text="Percentage",  # Keep text for display
                color_discrete_map={
                    "Non-Boundary Ball Percent": "#ff7f0e",  # Orange
                    "Boundary Ball Percent": "#2ca02c",  # Green
                    "Dot Ball Percent": "#1f77b4"  # Blue
                },
                barmode="stack",  # Stacked horizontal bars
                orientation="h",  # Horizontal orientation for correct order
            )

            fig_avg.update_layout(
                xaxis_title="Percentage",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),  # Reverse y-axis for correct order
                # xaxis=dict(
                #     range=[0, 100]  # Set x-axis range to 0-100%
                # )
            )

            fig_avg.update_traces(texttemplate='%{text:.1f}%', textposition='inside')

            st.plotly_chart(fig_avg)


        with col4:
            fig_boundaries = px.bar(
                data,
                y="Economy Rate",
                x="Bowler",
                color="Economy Rate",
                title="Economy Rate",
                color_continuous_scale="Blues",
            )
            fig_boundaries.update_layout(
                xaxis_title="",
                yaxis_title="Boundaries Hit",
                xaxis_tickangle=-90,
                yaxis = dict(categoryorder="total descending"
            )
            )
            st.plotly_chart(fig_boundaries)

    with tab2:
        # Dataframe for details
        st.subheader("Player Details")
        st.dataframe(data)

def bowler_performance(season, name):

    df = db.bowling_stats(season)
    data = df[df['Bowler'] == name]
    bbi = db.best_bowling_inning(season, name)
    bbi_metric = '{}/{}'.format(bbi['wickets_taken'].values[0],bbi['runs_conceded'].values[0])

    # KPI Metrics
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

    try:
        col1.metric("Innings", round(data["Matches Played"].values[0]))
        col2.metric("Balls", round(data["Total Balls"].values[0]))
        col3.metric("Runs", round(data["Total Runs Conceded"].values[0]))
        col4.metric("Wickets", round(data['Total Wickets'].values[0]))
        col5.metric("Bowling Avg", round(data['Bowling Average'].values[0]))
        col6.metric("Economy Rate", data['Economy Rate'].values[0])
        col7.metric("Strike Rate", data["Strike Rate"].values[0])
        col8.metric("Dot Ball %", round(data["Dot Ball Percent"].values[0]))
        col9.metric("Maidens", round(data["Total Maidens"].values[0]))
        col10.metric("BBI", bbi_metric)
    except:
        st.write('')

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
            team = db.fetch_player_team(season,name, 'bowler')
            st.dataframe(team)

        # line graph for over seasons wickets
        wickets = db.bowler_records_trend(name,season)
        if wickets.season.nunique() > 1:
            fig_runs = px.line(
                wickets,
                x="season",
                y="wickets",
                title="Wickets by Seasons",
                markers= 'o'
            )
            fig_runs.update_layout(
                yaxis_title="Wickets",
                xaxis_title="Season",
                yaxis=dict(categoryorder="total ascending")
            )
            st.plotly_chart(fig_runs)


        col3,col4 = st.columns([2,3])
        with col3:
            avg_sr = db.bowler_avg_sr(season,name)
            fig_runs = px.bar(
                avg_sr,
                x="opponent_name",
                y=["Bowling Average","Strike Rate"],
                title="Bowling Avg and SR Against Team",
                color_continuous_scale= 'Viridis',
                text_auto=True,
                barmode='group'
            )
            fig_runs.update_layout(
                xaxis_title="opponent Team",
                yaxis_title="Runs",
                yaxis=dict(categoryorder="total ascending"),
                height = 600
            )
            st.plotly_chart(fig_runs, use_container_width=True)

        with col4:
            data = db.bowler_records_trend(name,season)

            fig1_runs = px.scatter(
                data,
                x = 'season',
                y = 'wickets',
                size='Economy Rate',
                title='Wickets and Economy',
                color_continuous_scale='Virdis'
            )
            fig1_runs.update_layout(
                xaxis_title="Season",
                yaxis_title="Wickets",
                yaxis=dict(categoryorder="total ascending"),
                height=300
            )
            st.plotly_chart(fig1_runs, use_container_width=True)

            data = db.bowling_stats(season)
            bowling_dist = data[data['Bowler']=='Wahab Riaz'][['Dot Ball Percent','Boundary Ball Percent', 'Non-Boundary Ball Percent']].melt()

            fig2_runs = px.pie(
                bowling_dist,
                values='value',
                color = 'variable',
                title="Bowling Distribution",
                names='variable'
            )
            fig2_runs.update_layout(
                height = 300
            )
            st.plotly_chart(fig2_runs, use_container_width=True)

    with tab2:
        # Dataframe for details
        data = db.bowling_stats(season)
        bowler_details = data[data['Bowler']==name]
        st.subheader("Player Details")
        st.dataframe(bowler_details)