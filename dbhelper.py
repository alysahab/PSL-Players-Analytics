import streamlit as st
from sqlalchemy import create_engine
import pandas as pd


class DB:
    # connect to database
    def __init__(self):
        self.user = st.secrets.db_credentials.user
        self.password = st.secrets.db_credentials.password

        try:
            self.con = create_engine(f'mysql+pymysql://{self.user}:{self.password}@127.0.0.1/psl')
            print('established connection')
        except:
            print('connection error')

    def run_query(self, query):
        return pd.read_sql_query(query, self.con)

    def fetch_season(self):
        # Fetch unique seasons from the database
        seasons = self.run_query('SELECT DISTINCT season FROM batting_data')
        # Create a list with 'All Season' as the first entry, followed by the seasons
        data = ['All Season'] + sorted([season[0] for season in seasons.values])
        return data

    def player_season(self, name):
        # Fetch unique seasons from the database
        seasons = self.run_query('SELECT DISTINCT season FROM batting_data where batsman = "{}"'.format(name))
        # Create a list with 'All Season' as the first entry, followed by the seasons
        data = ['All Season'] + sorted([season[0] for season in seasons.values])
        return data

    def fetch_names(self):
        # Fetch batsman names from the database
        player = self.run_query('SELECT DISTINCT batsman FROM batting_data')
        data = ['choose a player'] + [player[0] for player in player.values]
        return data

    def fetch_players_record(self, season):
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

    def fetch_individual_overall(self, season, name):

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

    def fetch_dismissal_detail(self, name):
        data = self.run_query("""
            select batsman, dismissed_by as 'Bowlers', count(*) as 'no of Wicket'
            from batting_data
            where dismissed_by not in ('run out', 'not out') and batsman = 'Babar Azam'
            group by batsman, dismissed_by
            order by count(*) desc limit 5
        """)
        return data

    def fetch_player_team(self, season, name):

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

        # Display the result DataFrame
        return result_df

    def fetch_individual_record(self, name):
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
