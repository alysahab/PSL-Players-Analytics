import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import pymysql


class DB:
    # connect to database
    def __init__(self):
        ENDPOINT = st.secrets.host
        PORT = st.secrets.port
        USER = st.secrets.user
        PASSWORD = st.secrets.password
        DBNAME = st.secrets.DBname

        try:
            self.con = pymysql.connect(
                                        host=ENDPOINT,
                                        user=USER,
                                        password=PASSWORD,
                                        port=PORT,
                                        database=DBNAME
            )
        except:
            print('connection error')
            self.con = None

    def run_query(self, query):
        return pd.read_sql_query(query, self.con)

    def fetch_season(self):
        # Fetch unique seasons from the database
        seasons = self.run_query('SELECT DISTINCT season FROM batting_data')
        # Create a list with 'All Season' as the first entry, followed by the seasons
        data = ['All Season'] + sorted([season[0] for season in seasons.values])
        return data

    def batters_season(self, name):
        # Fetch unique seasons from the database
        seasons = self.run_query('SELECT DISTINCT season FROM batting_data where batsman = "{}"'.format(name))
        # Create a list with 'All Season' as the first entry, followed by the seasons
        data = ['All Season'] + sorted([season[0] for season in seasons.values])
        return data

    def bowlers_season(self, name):
        # Fetch unique seasons from the database
        seasons = self.run_query('SELECT DISTINCT season FROM bowling_data where bowler = "{}"'.format(name))
        # Create a list with 'All Season' as the first entry, followed by the seasons
        data = ['All Season'] + sorted([season[0] for season in seasons.values])
        return data

    def fetch_batters_names(self):
        # Fetch batsman names from the database
        player = self.run_query('SELECT DISTINCT batsman FROM batting_data')
        data = ['choose a player'] + [player[0] for player in player.values]
        return data
    def fetch_bowlers_names(self):
        # Fetch batsman names from the database
        player = self.run_query('SELECT Distinct bowler FROM bowling_data order by bowler')
        data = ['choose a player'] + [player[0] for player in player.values]
        return data

    def batters_df(self, season):
        if season == 'All Season':
            table = self.run_query("""
                        select batsman 'Batsman',
                        count(*) 'Matches Played',
                        sum(total_balls) as 'Balls faced', 
                        sum(total_runs) 'Runs scored', 
                        sum(fours+sixes) 'Boundaries hit', 
                        round((sum(total_runs)/sum(total_balls)) * 100,2) as 'Strike rate',
                        round(SUM(total_runs) / COUNT(CASE WHEN wicket_type != 'not out' THEN 1 END)) AS 'Batting Average'
                        from batting_data
                        group by batsman
                        order by sum(total_runs) desc
            """)
            return table
        else:
            table = self.run_query("""
                        select batsman 'Batsman',
                        team_name 'Team',
                        count(*) 'Matches Played',
                        sum(total_balls) as 'Balls faced',
                        sum(total_runs) 'Runs scored', 
                        sum(fours+sixes) 'Boundaries hit', 
                        round((sum(total_runs)/sum(total_balls)) * 100,2) as 'Strike rate',
                        round(SUM(total_runs) / COUNT(CASE WHEN wicket_type != 'not out' THEN 1 END)) AS 'Batting Average'
                        from batting_data
                        where season = '{}'
                        group by batsman, team_name
                        order by sum(total_runs) desc
                        """.format(season))
            return table

    def batter_metrics(self, season, name):

        if season == 'All Season':
            data = self.run_query("""
                select batsman,
                count(*) 'Match Played',
                sum(total_runs) 'Runs', 
                round((sum(total_runs)/sum(total_balls)) * 100,2) as 'Strike Rate',
                round(SUM(total_runs) / COUNT(CASE WHEN wicket_type != 'not out' THEN 1 END),2) AS 'Batting Average',
                sum(fours) 'fours',
                sum(sixes) 'sixes',
                count(case when total_runs >= 50 and total_runs < 100 then 1 end) '50s',
                count(case when total_runs >= 100 then 1 end) '100s'
                from batting_data
                where batsman = '{}'
                group by batsman;
            """.format(name))
            return data
        else:
            try:
                data = self.run_query("""
                select batsman,
                count(*) 'Match Played',
                sum(total_runs) 'Runs', 
                round((sum(total_runs)/sum(total_balls)) * 100,2) as 'Strike Rate',
                round(SUM(total_runs) / COUNT(CASE WHEN wicket_type != 'not out' THEN 1 END)) AS 'Batting Average',
                sum(fours) 'fours',
                sum(sixes) 'sixes',
                count(case when total_runs >= 50 and total_runs < 100 then 1 end) '50s',
                count(case when total_runs >= 100 then 1 end) '100s'
                from batting_data
                where batsman = '{}' and season = {}
                group by batsman;
                            """.format(name, season))
                return data
            except:
                return 'Have zero matches in {}'.format(season)

    def fetch_player_overview(self, name):
        data = self.run_query("""
            select bat.batsman 'Player',
            info.position 'Playing role',
            info.batting_style 'Batting style',
            case when info.bowling_style is not null then bowling_style else 'nill' end as 'Bowling style'
            from batting_data bat
            join players_info info
            on bat.batsman = info.names
            where bat.batsman = '{}'
            group by bat.batsman,info.position, info.batting_style, 
            case when info.bowling_style is not null then bowling_style else 'nill' end; 
        """.format(name))
        return data

    def fetch_player_team(self, season, name, player):


        if player == 'batter':
            if season == 'All Season':
                data = self.run_query("""
                                SELECT batsman, season, team_name
                                FROM batting_data
                                WHERE batsman = '{}'
                                GROUP BY batsman, season, team_name
                """.format(name))
            else:
                data = self.run_query("""
                                SELECT batsman, season, team_name
                                FROM batting_data
                                WHERE batsman = '{}' and season = {}
                                GROUP BY batsman, season, team_name
                            """.format(name, season))
        else:
            if season == 'All Season':
                data = self.run_query("""
                                SELECT bowler, season, team_name
                                FROM bowling_data
                                WHERE bowler = '{}'
                                GROUP BY bowler, season, team_name
                """.format(name))
            else:
                data = self.run_query("""
                                SELECT bowler, season, team_name
                                FROM bowling_data
                                WHERE bowler = '{}' and season = {}
                                GROUP BY bowler, season, team_name
                            """.format(name, season))


        # Create and sort the DataFrame
        df = pd.DataFrame(data).sort_values(by="season").reset_index(drop=True)

        # Initialize a result list for constructing the new DataFrame
        result = []

        if df["team_name"].nunique() > 1:
            season1 = df.loc[0, "season"]
            team1 = df.loc[0, "team_name"]
            count = 0

            for i in range(1, len(df)):
                team2 = df.loc[i, "team_name"]
                season2 = df.loc[i, "season"]

                if team2 == team1:
                    count += 1
                else:
                    if count == 0:
                        result.append({"Season": f"{season1}", "Team": team1})
                    else:
                        result.append({"Season": f"{season1}-{season2 - 1}", "Team": team1})

                    # Update the tracking variables
                    season1 = season2
                    team1 = team2
                    count = 0

                # Handle the last season for the final team
                if i == len(df) - 1:
                    if count == 0:
                        result.append({"Season": f"{season1}", "Team": team1})
                    else:
                        result.append({"Season": f"{season1}-{season2}", "Team": team1})
        else:
            if df.season.nunique() > 1:
                # Single team for all seasons
                result.append({"Season": f"{df.iloc[0, 1]}-{df.iloc[-1, 1]}", "Team": df["team_name"].iloc[0]})
            else:
                # If only played for 1 season
                result.append({"Season": f"{df.iloc[0, 1]}", "Team": df["team_name"].iloc[0]})

        # Create the result DataFrame
        result_df = pd.DataFrame(result)

        # return the result DataFrame
        return result_df

    def individual_batter_record(self, name):
        data = self.run_query("""
            select season as 'Season', team_name 'Team Name',
                        count(*) 'Matches Played',
                        sum(total_balls) as 'Balls faced', 
                        sum(total_runs) 'Runs scored',
                        sum(fours) 'fours',
						sum(sixes) 'sixes',
                        sum(fours+sixes) 'Total Boundaries', 
                        round((sum(total_runs)/sum(total_balls)) * 100,2) as 'Strike rate',
                        round(SUM(total_runs) / COUNT(CASE WHEN wicket_type != 'not out' THEN 1 END)) AS 'Batting Average',
                        count(case when total_runs >= 50 and total_runs < 100 then 1 end) '50s',
						count(case when total_runs >= 100 then 1 end) '100s'
                        from batting_data
                        where Batsman = '{}'
                        group by batsman, season, team_name
                        order by season
        """.format(name))
        return data

    def run_against_team(self, season, name):
        if season == 'All Season':
            data = self.run_query("""
                        select batsman,opponent_team,sum(total_runs) 'runs'
                        from batting_data
                        where batsman= '{}'
                        group by batsman,opponent_team
            """.format(name))
            return data
        else:
            data = self.run_query("""
                                    select batsman,opponent_team,sum(total_runs) 'runs'
                                    from batting_data
                                    where batsman= '{}' and season = {}
                                    group by batsman,opponent_team
                        """.format(name, season))
            return data

    def player_dismissal(self, season,name):
        if season == 'All Season':
            data = self.run_query("""
                        select batsman, dismissed_by, count(dismissed_by) 'wickets'
                        from batting_data
                        where dismissed_by not in ('not out', 'run out') and batsman = '{}'
                        group by batsman, dismissed_by
                        order by wickets desc limit 5;""".format(name))
            return data
        else:
            data = self.run_query("""
                                    select batsman, dismissed_by, count(dismissed_by) 'wickets'
                                    from batting_data
                                    where dismissed_by not in ('not out', 'run out') and batsman = '{}' and season = {}
                                    group by batsman, dismissed_by
                                    order by wickets desc limit 5;""".format(name,season))
            return data

    def player_wicket_type(self,season,name):
        if season == 'All Season':
            data = self.run_query("""
                        select batsman, wicket_type, count(wicket_type) 'wickets'
                        from batting_data
                        where wicket_type not in ('not out') and batsman = '{}'
                        group by batsman, wicket_type
                        order by wickets desc
            """.format(name))
            return data
        else:
            data = self.run_query("""
                                    select batsman, wicket_type, count(wicket_type) 'wickets'
                                    from batting_data
                                    where wicket_type not in ('not out') and batsman = '{}' and season = {}
                                    group by batsman, wicket_type
                                    order by wickets desc
                        """.format(name,season))
            return data

    def bowling_stats(self, season):

        if season == 'All Season':
            data = self.run_query("""
                    SELECT 
                        bowler AS 'Bowler',
                        -- Total Match
                        COUNT(*) as 'Matches Played',
                        -- Total Balls
                        SUM(total_balls) 'Total Balls',
                        -- Total wickets taken by the bowler
                        SUM(wickets_taken) AS 'Total Wickets',
                        -- Bowling Average: Runs conceded per wicket taken
                        ROUND(SUM(runs_conceded) / SUM(wickets_taken), 2) AS 'Bowling Average',
                        -- Economy Rate: Runs conceded per over bowled
                        ROUND(SUM(runs_conceded) / SUM(overs), 2) AS 'Economy Rate',
                        -- Bowling Strike Rate: Balls bowled per wicket taken
                        ROUND(SUM(total_balls) / SUM(wickets_taken)) AS 'Strike Rate',
                        -- Dot Ball Percentage: Percentage of dot balls bowled
                        ROUND((SUM(dot_balls) / SUM(total_balls)) * 100, 2) AS 'Dot Ball Percent',
                        -- Boundary Percentage: Percentage of balls that resulted in boundaries
                        ROUND(((SUM(fours_conceded) + SUM(sixes_conceded)) / SUM(total_balls)) * 100, 2) AS 'Boundary Ball Percent',
                        100 - ((ROUND((SUM(dot_balls) / SUM(total_balls)) * 100, 2)) + 
                        (ROUND(((SUM(fours_conceded) + SUM(sixes_conceded)) / SUM(total_balls)) * 100, 2))) AS 'Non-Boundary Ball Percent',
                        -- Total runs conceded by the bowler
                        SUM(runs_conceded) AS 'Total Runs Conceded',
                        -- Total maiden overs bowled
                        SUM(maidens) AS 'Total Maidens',
                        -- Total extras conceded (wides + no balls)
                        SUM(wide_balls) + SUM(no_balls) AS 'Total Extras Conceded',
                        count(case when wickets_taken = 4 then 1 end) '4W',
                        count(case when wickets_taken >= 5 then 1 end) '5W'
                    FROM 
                        bowling_data
                    GROUP BY 
                        bowler
                    ORDER BY 
                        SUM(wickets_taken) DESC;
            """)
            return data
        else:
            data = self.run_query("""
                    SELECT 
                        bowler AS 'Bowler',
                        -- Total Match
                        COUNT(*) as 'Matches Played',
                        -- Total Balls
                        SUM(total_balls) 'Total Balls',
                        -- Total wickets taken by the bowler
                        SUM(wickets_taken) AS 'Total Wickets',
                        -- Bowling Average: Runs conceded per wicket taken
                        ROUND(SUM(runs_conceded) / SUM(wickets_taken), 2) AS 'Bowling Average',
                        -- Economy Rate: Runs conceded per over bowled
                        ROUND(SUM(runs_conceded) / SUM(overs), 2) AS 'Economy Rate',
                        -- Bowling Strike Rate: Balls bowled per wicket taken
                        ROUND(SUM(total_balls) / SUM(wickets_taken)) AS 'Strike Rate',
                        -- Dot Ball Percentage: Percentage of dot balls bowled
                        ROUND((SUM(dot_balls) / SUM(total_balls)) * 100, 2) AS 'Dot Ball Percent',
                        -- Total maiden overs bowled
                        SUM(maidens) AS 'Total Maidens',
                        -- Boundary Percentage: Percentage of balls that resulted in boundaries
                        ROUND(((SUM(fours_conceded) + SUM(sixes_conceded)) / SUM(total_balls)) * 100, 2) AS 'Boundary Ball Percent',
                        100 - ((ROUND((SUM(dot_balls) / SUM(total_balls)) * 100, 2)) + 
                        (ROUND(((SUM(fours_conceded) + SUM(sixes_conceded)) / SUM(total_balls)) * 100, 2))) AS 'Non-Boundary Ball Percent',
                        -- Total runs conceded by the bowler
                        SUM(runs_conceded) AS 'Total Runs Conceded',
                        -- Total extras conceded (wides + no balls)
                        SUM(wide_balls) + SUM(no_balls) AS 'Total Extras Conceded',
                        count(case when wickets_taken = 4 then 1 end) '4W',
                        count(case when wickets_taken >= 5 then 1 end) '5W'
                    FROM 
                        bowling_data
                    WHERE season = {}
                    GROUP BY 
                        bowler
                    ORDER BY 
                        SUM(wickets_taken) DESC;               
                """.format(season))
            return data
    def best_bowling_inning(self, season, name):
        if season == 'All Season':
            data = self.run_query(f"""
            WITH bbi AS (
                    SELECT 
                        bowler, 
                        wickets_taken, 
                        runs_conceded,
                        ROW_NUMBER() OVER (PARTITION BY bowler ORDER BY wickets_taken DESC, runs_conceded ASC) AS rk
                    FROM bowling_data
                    where bowler = '{name}'
                    )
                    SELECT bowler, wickets_taken, runs_conceded
                    FROM bbi
                    WHERE rk = 1;
            
            """)
            return data

        else:
            data = self.run_query(f"""
                        WITH bbi AS (
                                SELECT 
                                    bowler, 
                                    wickets_taken, 
                                    runs_conceded,
                                    ROW_NUMBER() OVER (PARTITION BY bowler ORDER BY wickets_taken DESC, runs_conceded ASC) AS rk
                                FROM bowling_data
                                WHERE bowler = '{name}' and season = {season}
                                )
                                SELECT bowler, wickets_taken, runs_conceded
                                FROM bbi
                                WHERE rk = 1;

                        """)
            return data
    def bowler_records_trend(self,name,season):

        if season == 'All Season':
            data = self.run_query("""
                    select bowler, season,
                    sum(wickets_taken) as wickets,
                    ROUND(SUM(runs_conceded) / SUM(overs), 2) AS 'Economy Rate'
                    from bowling_data
                    where bowler = '{}'
                    group by bowler, season;
            """.format(name))
            return data
        else:
            data = self.run_query("""
                                select bowler, season,
                                sum(wickets_taken) as wickets,
                                ROUND(SUM(runs_conceded) / SUM(overs), 2) AS 'Economy Rate'
                                from bowling_data
                                where bowler = '{}' and season = {}
                                group by bowler, season;
                        """.format(name,season))
            return data


    def bowler_avg_sr(self,season,name):
        if season == 'All Season':
            data = self.run_query("""
                    select bowler,opponent_name,
                        ROUND(SUM(runs_conceded) / SUM(wickets_taken), 2) AS 'Bowling Average',
                        ROUND(SUM(total_balls) / SUM(wickets_taken), 2) AS 'Strike Rate'
                        from bowling_data
                        where bowler = '{}'
                        group by bowler,opponent_name
            """.format(name))
            return data
        else:
            data = self.run_query("""
                                select bowler,opponent_name,
                                    ROUND(SUM(runs_conceded) / SUM(wickets_taken), 2) AS 'Bowling Average',
                                    ROUND(SUM(total_balls) / SUM(wickets_taken), 2) AS 'Strike Rate'
                                    from bowling_data
                                    where bowler = '{}' and season = {}
                                    group by bowler,opponent_name
                        """.format(name, season))
            return data

