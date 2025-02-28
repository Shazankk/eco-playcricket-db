# Description: This file contains the SQL queries to initialize the database.
import sqlite3
import os
from dotenv import load_dotenv
import libsql_experimental as libsql

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
    raise ValueError("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in the environment variables")

# if os.path.exists('colchestercavs.db'):
#     os.remove('colchestercavs.db')

competition_teams = f"""
CREATE TABLE IF NOT EXISTS competition_teams (
        club_id INTEGER,
        club_name TEXT,
        team_id INTEGER PRIMARY KEY,
        team_name TEXT,
        league_id INTEGER
    )
"""

fixtures = f"""
CREATE TABLE IF NOT EXISTS fixtures (
        id INTEGER PRIMARY KEY,
        status TEXT,
        published TEXT,
        last_updated TEXT,
        league_name TEXT,
        league_id INTEGER,
        competition_name TEXT,
        competition_id INTEGER,
        competition_type TEXT,
        match_type TEXT,
        game_type TEXT,
        season INTEGER,
        match_date TEXT,
        match_time TEXT,
        ground_name TEXT,
        ground_id INTEGER,
        ground_latitude TEXT,
        ground_longitude TEXT,
        home_club_name TEXT,
        home_team_name TEXT,
        home_team_id INTEGER,
        home_club_id INTEGER,
        away_club_name TEXT,
        away_team_name TEXT,
        away_team_id INTEGER,
        away_club_id INTEGER,
        umpire_1_name TEXT,
        umpire_1_id TEXT,
        umpire_2_name TEXT,
        umpire_2_id TEXT,
        umpire_3_name TEXT,
        umpire_3_id TEXT,
        referee_name TEXT,
        referee_id TEXT,
        scorer_1_name TEXT,
        scorer_1_id TEXT,
        scorer_2_name TEXT,
        scorer_2_id TEXT
    )
"""

players = f"""
CREATE TABLE IF NOT EXISTS players (
            member_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
"""

result_summary = f"""
CREATE TABLE IF NOT EXISTS result_summary (
        id INTEGER PRIMARY KEY,
        status TEXT,
        published TEXT,
        last_updated TEXT,
        league_name TEXT,
        league_id TEXT,
        competition_name TEXT,
        competition_id TEXT,
        competition_type TEXT,
        match_type TEXT,
        game_type TEXT,
        countdown_cricket TEXT,
        match_date TEXT,
        match_time TEXT,
        ground_name TEXT,
        ground_id TEXT,
        home_team_name TEXT,
        home_team_id TEXT,
        home_club_name TEXT,
        home_club_id TEXT,
        away_team_name TEXT,
        away_team_id TEXT,
        away_club_name TEXT,
        away_club_id TEXT,
        umpire_1_name TEXT,
        umpire_1_id TEXT,
        umpire_2_name TEXT,
        umpire_2_id TEXT,
        umpire_3_name TEXT,
        umpire_3_id TEXT,
        referee_name TEXT,
        referee_id TEXT,
        scorer_1_name TEXT,
        scorer_1_id TEXT,
        scorer_2_name TEXT,
        scorer_2_id TEXT,
        toss_won_by_team_id TEXT,
        toss TEXT,
        batted_first TEXT,
        no_of_overs TEXT,
        balls_per_innings TEXT,
        no_of_innings TEXT,
        result TEXT,
        result_description TEXT,
        result_applied_to TEXT,
        home_confirmed TEXT,
        away_confirmed TEXT,
        result_locked TEXT,
        scorecard_locked TEXT,
        match_notes TEXT,
        points_0_team_id INTEGER,
        points_0_game_points TEXT,
        points_0_penalty_points TEXT,
        points_0_bonus_points_together TEXT,
        points_0_bonus_points_batting TEXT,
        points_0_bonus_points_bowling TEXT,
        points_0_bonus_points_2nd_innings_together TEXT,
        points_1_team_id INTEGER,
        points_1_game_points TEXT,
        points_1_penalty_points TEXT,
        points_1_bonus_points_together TEXT,
        points_1_bonus_points_batting TEXT,
        points_1_bonus_points_bowling TEXT,
        points_1_bonus_points_2nd_innings_together TEXT,
        innings_0_team_batting_id TEXT,
        innings_0_innings_number INTEGER,
        innings_0_extra_byes TEXT,
        innings_0_extra_leg_byes TEXT,
        innings_0_extra_wides TEXT,
        innings_0_extra_no_balls TEXT,
        innings_0_extra_penalty_runs TEXT,
        innings_0_penalties_runs_awarded_in_other_innings TEXT,
        innings_0_total_extras TEXT,
        innings_0_runs TEXT,
        innings_0_wickets TEXT,
        innings_0_overs TEXT,
        innings_0_balls TEXT,
        innings_0_declared BOOLEAN,
        innings_0_forfeited_innings BOOLEAN,
        innings_0_revised_target_runs TEXT,
        innings_0_revised_target_overs TEXT,
        innings_0_revised_target_balls TEXT,
        innings_1_team_batting_id TEXT,
        innings_1_innings_number INTEGER,
        innings_1_extra_byes TEXT,
        innings_1_extra_leg_byes TEXT,
        innings_1_extra_wides TEXT,
        innings_1_extra_no_balls TEXT,
        innings_1_extra_penalty_runs TEXT,
        innings_1_penalties_runs_awarded_in_other_innings TEXT,
        innings_1_total_extras TEXT,
        innings_1_runs TEXT,
        innings_1_wickets TEXT,
        innings_1_overs TEXT,
        innings_1_balls TEXT,
        innings_1_declared BOOLEAN,
        innings_1_forfeited_innings BOOLEAN,
        innings_1_revised_target_runs TEXT,
        innings_1_revised_target_overs TEXT,
        innings_1_revised_target_balls TEXT
    )
"""

teams = f"""
CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        status TEXT,
        last_updated TEXT,
        site_id INTEGER,
        team_name TEXT,
        other_team_name TEXT,
        nickname TEXT,
        team_captain TEXT
    )
"""

# match_details = f"""
# CREATE TABLE IF NOT EXISTS match_details (
#   id TEXT,
#   status TEXT,
#   published TEXT,
#   last_updated TEXT,
#   league_name TEXT,
#   league_id TEXT,
#   competition_name TEXT,
#   competition_id TEXT,
#   competition_type TEXT,
#   match_type TEXT,
#   game_type TEXT,
#   countdown_cricket TEXT,
#   match_id TEXT,
#   match_date TEXT,
#   match_time TEXT,
#   ground_name TEXT,
#   ground_id TEXT,
#   home_team_name TEXT,
#   home_team_id TEXT,
#   home_club_name TEXT,
#   home_club_id TEXT,
#   away_team_name TEXT,
#   away_team_id TEXT,
#   away_club_name TEXT,
#   away_club_id TEXT,
#   umpire_1_name TEXT,
#   umpire_1_id TEXT,
#   umpire_2_name TEXT,
#   umpire_2_id TEXT,
#   umpire_3_name TEXT,
#   umpire_3_id TEXT,
#   referee_name TEXT,
#   referee_id TEXT,
#   scorer_1_name TEXT,
#   scorer_1_id TEXT,
#   scorer_2_name TEXT,
#   scorer_2_id TEXT,
#   toss_won_by_team_id TEXT,
#   toss TEXT,
#   batted_first TEXT,
#   no_of_overs TEXT,
#   balls_per_innings TEXT,
#   no_of_innings TEXT,
#   no_of_days TEXT,
#   no_of_players TEXT,
#   no_of_reserves TEXT,
#   result TEXT,
#   result_description TEXT,
#   result_applied_to TEXT,
#   match_notes TEXT,
#   points_0_team_id TEXT,
#   points_0_game_points TEXT,
#   points_0_penalty_points TEXT,
#   points_0_bonus_points_together TEXT,
#   points_0_bonus_points_batting TEXT,
#   points_0_bonus_points_bowling TEXT,
#   points_0_bonus_points_2nd_innings_together TEXT,
#   points_1_team_id TEXT,
#   points_1_game_points TEXT,
#   points_1_penalty_points TEXT,
#   points_1_bonus_points_together TEXT,
#   points_1_bonus_points_batting TEXT,
#   points_1_bonus_points_bowling TEXT,
#   points_1_bonus_points_2nd_innings_together TEXT,
#   match_result_types_0_0 TEXT,
#   match_result_types_0_1 TEXT,
#   match_result_types_1_0 TEXT,
#   match_result_types_1_1 TEXT,
#   match_result_types_2_0 TEXT,
#   match_result_types_2_1 TEXT,
#   match_result_types_3_0 TEXT,
#   match_result_types_3_1 TEXT,
#   match_result_types_4_0 TEXT,
#   match_result_types_4_1 TEXT,
#   match_result_types_5_0 TEXT,
#   match_result_types_5_1 TEXT,
#   match_result_types_6_0 TEXT,
#   match_result_types_6_1 TEXT,
#   match_result_types_7_0 TEXT,
#   match_result_types_7_1 TEXT,
#   players_0_home_team_0_position TEXT,
#   players_0_home_team_0_player_name TEXT,
#   players_0_home_team_0_player_id TEXT,
#   players_0_home_team_0_captain TEXT,
#   players_0_home_team_0_wicket_keeper TEXT,
#   players_0_home_team_1_position TEXT,
#   players_0_home_team_1_player_name TEXT,
#   players_0_home_team_1_player_id TEXT,
#   players_0_home_team_1_captain TEXT,
#   players_0_home_team_1_wicket_keeper TEXT,
#   players_0_home_team_2_position TEXT,
#   players_0_home_team_2_player_name TEXT,
#   players_0_home_team_2_player_id TEXT,
#   players_0_home_team_2_captain TEXT,
#   players_0_home_team_2_wicket_keeper TEXT,
#   players_0_home_team_3_position TEXT,
#   players_0_home_team_3_player_name TEXT,
#   players_0_home_team_3_player_id TEXT,
#   players_0_home_team_3_captain TEXT,
#   players_0_home_team_3_wicket_keeper TEXT,
#   players_0_home_team_4_position TEXT,
#   players_0_home_team_4_player_name TEXT,
#   players_0_home_team_4_player_id TEXT,
#   players_0_home_team_4_captain TEXT,
#   players_0_home_team_4_wicket_keeper TEXT,
#   players_0_home_team_5_position TEXT,
#   players_0_home_team_5_player_name TEXT,
#   players_0_home_team_5_player_id TEXT,
#   players_0_home_team_5_captain TEXT,
#   players_0_home_team_5_wicket_keeper TEXT,
#   players_0_home_team_6_position TEXT,
#   players_0_home_team_6_player_name TEXT,
#   players_0_home_team_6_player_id TEXT,
#   players_0_home_team_6_captain TEXT,
#   players_0_home_team_6_wicket_keeper TEXT,
#   players_0_home_team_7_position TEXT,
#   players_0_home_team_7_player_name TEXT,
#   players_0_home_team_7_player_id TEXT,
#   players_0_home_team_7_captain TEXT,
#   players_0_home_team_7_wicket_keeper TEXT,
#   players_0_home_team_8_position TEXT,
#   players_0_home_team_8_player_name TEXT,
#   players_0_home_team_8_player_id TEXT,
#   players_0_home_team_8_captain TEXT,
#   players_0_home_team_8_wicket_keeper TEXT,
#   players_0_home_team_9_position TEXT,
#   players_0_home_team_9_player_name TEXT,
#   players_0_home_team_9_player_id TEXT,
#   players_0_home_team_9_captain TEXT,
#   players_0_home_team_9_wicket_keeper TEXT,
#   players_0_home_team_10_position TEXT,
#   players_0_home_team_10_player_name TEXT,
#   players_0_home_team_10_player_id TEXT,
#   players_0_home_team_10_captain TEXT,
#   players_0_home_team_10_wicket_keeper TEXT,
#   players_1_away_team_0_position TEXT,
#   players_1_away_team_0_player_name TEXT,
#   players_1_away_team_0_player_id TEXT,
#   players_1_away_team_0_captain TEXT,
#   players_1_away_team_0_wicket_keeper TEXT,
#   players_1_away_team_1_position TEXT,
#   players_1_away_team_1_player_name TEXT,
#   players_1_away_team_1_player_id TEXT,
#   players_1_away_team_1_captain TEXT,
#   players_1_away_team_1_wicket_keeper TEXT,
#   players_1_away_team_2_position TEXT,
#   players_1_away_team_2_player_name TEXT,
#   players_1_away_team_2_player_id TEXT,
#   players_1_away_team_2_captain TEXT,
#   players_1_away_team_2_wicket_keeper TEXT,
#   players_1_away_team_3_position TEXT,
#   players_1_away_team_3_player_name TEXT,
#   players_1_away_team_3_player_id TEXT,
#   players_1_away_team_3_captain TEXT,
#   players_1_away_team_3_wicket_keeper TEXT,
#   players_1_away_team_4_position TEXT,
#   players_1_away_team_4_player_name TEXT,
#   players_1_away_team_4_player_id TEXT,
#   players_1_away_team_4_captain TEXT,
#   players_1_away_team_4_wicket_keeper TEXT,
#   players_1_away_team_5_position TEXT,
#   players_1_away_team_5_player_name TEXT,
#   players_1_away_team_5_player_id TEXT,
#   players_1_away_team_5_captain TEXT,
#   players_1_away_team_5_wicket_keeper TEXT,
#   players_1_away_team_6_position TEXT,
#   players_1_away_team_6_player_name TEXT,
#   players_1_away_team_6_player_id TEXT,
#   players_1_away_team_6_captain TEXT,
#   players_1_away_team_6_wicket_keeper TEXT,
#   players_1_away_team_7_position TEXT,
#   players_1_away_team_7_player_name TEXT,
#   players_1_away_team_7_player_id TEXT,
#   players_1_away_team_7_captain TEXT,
#   players_1_away_team_7_wicket_keeper TEXT,
#   players_1_away_team_8_position TEXT,
#   players_1_away_team_8_player_name TEXT,
#   players_1_away_team_8_player_id TEXT,
#   players_1_away_team_8_captain TEXT,
#   players_1_away_team_8_wicket_keeper TEXT,
#   players_1_away_team_9_position TEXT,
#   players_1_away_team_9_player_name TEXT,
#   players_1_away_team_9_player_id TEXT,
#   players_1_away_team_9_captain TEXT,
#   players_1_away_team_9_wicket_keeper TEXT,
#   players_1_away_team_10_position TEXT,
#   players_1_away_team_10_player_name TEXT,
#   players_1_away_team_10_player_id TEXT,
#   players_1_away_team_10_captain TEXT,
#   players_1_away_team_10_wicket_keeper TEXT,
#   innings_0_team_batting_name TEXT,
#   innings_0_team_batting_id TEXT,
#   innings_0_innings_number TEXT,
#   innings_0_extra_byes TEXT,
#   innings_0_extra_leg_byes TEXT,
#   innings_0_extra_wides TEXT,
#   innings_0_extra_no_balls TEXT,
#   innings_0_extra_penalty_runs TEXT,
#   innings_0_penalties_runs_awarded_in_other_innings TEXT,
#   innings_0_total_extras TEXT,
#   innings_0_runs TEXT,
#   innings_0_wickets TEXT,
#   innings_0_overs TEXT,
#   innings_0_balls TEXT,
#   innings_0_declared TEXT,
#   innings_0_forfeited_innings TEXT,
#   innings_0_revised_target_runs TEXT,
#   innings_0_revised_target_overs TEXT,
#   innings_0_revised_target_balls TEXT,
#   innings_0_bat_0_position TEXT,
#   innings_0_bat_0_batsman_name TEXT,
#   innings_0_bat_0_batsman_id TEXT,
#   innings_0_bat_0_how_out TEXT,
#   innings_0_bat_0_fielder_name TEXT,
#   innings_0_bat_0_fielder_id TEXT,
#   innings_0_bat_0_bowler_name TEXT,
#   innings_0_bat_0_bowler_id TEXT,
#   innings_0_bat_0_runs TEXT,
#   innings_0_bat_0_fours TEXT,
#   innings_0_bat_0_sixes TEXT,
#   innings_0_bat_0_balls TEXT,
#   innings_0_bat_1_position TEXT,
#   innings_0_bat_1_batsman_name TEXT,
#   innings_0_bat_1_batsman_id TEXT,
#   innings_0_bat_1_how_out TEXT,
#   innings_0_bat_1_fielder_name TEXT,
#   innings_0_bat_1_fielder_id TEXT,
#   innings_0_bat_1_bowler_name TEXT,
#   innings_0_bat_1_bowler_id TEXT,
#   innings_0_bat_1_runs TEXT,
#   innings_0_bat_1_fours TEXT,
#   innings_0_bat_1_sixes TEXT,
#   innings_0_bat_1_balls TEXT,
#   innings_0_bat_2_position TEXT,
#   innings_0_bat_2_batsman_name TEXT,
#   innings_0_bat_2_batsman_id TEXT,
#   innings_0_bat_2_how_out TEXT,
#   innings_0_bat_2_fielder_name TEXT,
#   innings_0_bat_2_fielder_id TEXT,
#   innings_0_bat_2_bowler_name TEXT,
#   innings_0_bat_2_bowler_id TEXT,
#   innings_0_bat_2_runs TEXT,
#   innings_0_bat_2_fours TEXT,
#   innings_0_bat_2_sixes TEXT,
#   innings_0_bat_2_balls TEXT,
#   innings_0_bat_3_position TEXT,
#   innings_0_bat_3_batsman_name TEXT,
#   innings_0_bat_3_batsman_id TEXT,
#   innings_0_bat_3_how_out TEXT,
#   innings_0_bat_3_fielder_name TEXT,
#   innings_0_bat_3_fielder_id TEXT,
#   innings_0_bat_3_bowler_name TEXT,
#   innings_0_bat_3_bowler_id TEXT,
#   innings_0_bat_3_runs TEXT,
#   innings_0_bat_3_fours TEXT,
#   innings_0_bat_3_sixes TEXT,
#   innings_0_bat_3_balls TEXT,
#   innings_0_bat_4_position TEXT,
#   innings_0_bat_4_batsman_name TEXT,
#   innings_0_bat_4_batsman_id TEXT,
#   innings_0_bat_4_how_out TEXT,
#   innings_0_bat_4_fielder_name TEXT,
#   innings_0_bat_4_fielder_id TEXT,
#   innings_0_bat_4_bowler_name TEXT,
#   innings_0_bat_4_bowler_id TEXT,
#   innings_0_bat_4_runs TEXT,
#   innings_0_bat_4_fours TEXT,
#   innings_0_bat_4_sixes TEXT,
#   innings_0_bat_4_balls TEXT,
#   innings_0_bat_5_position TEXT,
#   innings_0_bat_5_batsman_name TEXT,
#   innings_0_bat_5_batsman_id TEXT,
#   innings_0_bat_5_how_out TEXT,
#   innings_0_bat_5_fielder_name TEXT,
#   innings_0_bat_5_fielder_id TEXT,
#   innings_0_bat_5_bowler_name TEXT,
#   innings_0_bat_5_bowler_id TEXT,
#   innings_0_bat_5_runs TEXT,
#   innings_0_bat_5_fours TEXT,
#   innings_0_bat_5_sixes TEXT,
#   innings_0_bat_5_balls TEXT,
#   innings_0_bat_6_position TEXT,
#   innings_0_bat_6_batsman_name TEXT,
#   innings_0_bat_6_batsman_id TEXT,
#   innings_0_bat_6_how_out TEXT,
#   innings_0_bat_6_fielder_name TEXT,
#   innings_0_bat_6_fielder_id TEXT,
#   innings_0_bat_6_bowler_name TEXT,
#   innings_0_bat_6_bowler_id TEXT,
#   innings_0_bat_6_runs TEXT,
#   innings_0_bat_6_fours TEXT,
#   innings_0_bat_6_sixes TEXT,
#   innings_0_bat_6_balls TEXT,
#   innings_0_bat_7_position TEXT,
#   innings_0_bat_7_batsman_name TEXT,
#   innings_0_bat_7_batsman_id TEXT,
#   innings_0_bat_7_how_out TEXT,
#   innings_0_bat_7_fielder_name TEXT,
#   innings_0_bat_7_fielder_id TEXT,
#   innings_0_bat_7_bowler_name TEXT,
#   innings_0_bat_7_bowler_id TEXT,
#   innings_0_bat_7_runs TEXT,
#   innings_0_bat_7_fours TEXT,
#   innings_0_bat_7_sixes TEXT,
#   innings_0_bat_7_balls TEXT,
#   innings_0_bat_8_position TEXT,
#   innings_0_bat_8_batsman_name TEXT,
#   innings_0_bat_8_batsman_id TEXT,
#   innings_0_bat_8_how_out TEXT,
#   innings_0_bat_8_fielder_name TEXT,
#   innings_0_bat_8_fielder_id TEXT,
#   innings_0_bat_8_bowler_name TEXT,
#   innings_0_bat_8_bowler_id TEXT,
#   innings_0_bat_8_runs TEXT,
#   innings_0_bat_8_fours TEXT,
#   innings_0_bat_8_sixes TEXT,
#   innings_0_bat_8_balls TEXT,
#   innings_0_bat_9_position TEXT,
#   innings_0_bat_9_batsman_name TEXT,
#   innings_0_bat_9_batsman_id TEXT,
#   innings_0_bat_9_how_out TEXT,
#   innings_0_bat_9_fielder_name TEXT,
#   innings_0_bat_9_fielder_id TEXT,
#   innings_0_bat_9_bowler_name TEXT,
#   innings_0_bat_9_bowler_id TEXT,
#   innings_0_bat_9_runs TEXT,
#   innings_0_bat_9_fours TEXT,
#   innings_0_bat_9_sixes TEXT,
#   innings_0_bat_9_balls TEXT,
#   innings_0_bat_10_position TEXT,
#   innings_0_bat_10_batsman_name TEXT,
#   innings_0_bat_10_batsman_id TEXT,
#   innings_0_bat_10_how_out TEXT,
#   innings_0_bat_10_fielder_name TEXT,
#   innings_0_bat_10_fielder_id TEXT,
#   innings_0_bat_10_bowler_name TEXT,
#   innings_0_bat_10_bowler_id TEXT,
#   innings_0_bat_10_runs TEXT,
#   innings_0_bat_10_fours TEXT,
#   innings_0_bat_10_sixes TEXT,
#   innings_0_bat_10_balls TEXT,
#   innings_0_fow_0_runs TEXT,
#   innings_0_fow_0_wickets TEXT,
#   innings_0_fow_0_batsman_out_name TEXT,
#   innings_0_fow_0_batsman_out_id TEXT,
#   innings_0_fow_0_batsman_in_name TEXT,
#   innings_0_fow_0_batsman_in_id TEXT,
#   innings_0_fow_0_batsman_in_runs TEXT,
#   innings_0_fow_1_runs TEXT,
#   innings_0_fow_1_wickets TEXT,
#   innings_0_fow_1_batsman_out_name TEXT,
#   innings_0_fow_1_batsman_out_id TEXT,
#   innings_0_fow_1_batsman_in_name TEXT,
#   innings_0_fow_1_batsman_in_id TEXT,
#   innings_0_fow_1_batsman_in_runs TEXT,
#   innings_0_fow_2_runs TEXT,
#   innings_0_fow_2_wickets TEXT,
#   innings_0_fow_2_batsman_out_name TEXT,
#   innings_0_fow_2_batsman_out_id TEXT,
#   innings_0_fow_2_batsman_in_name TEXT,
#   innings_0_fow_2_batsman_in_id TEXT,
#   innings_0_fow_2_batsman_in_runs TEXT,
#   innings_0_fow_3_runs TEXT,
#   innings_0_fow_3_wickets TEXT,
#   innings_0_fow_3_batsman_out_name TEXT,
#   innings_0_fow_3_batsman_out_id TEXT,
#   innings_0_fow_3_batsman_in_name TEXT,
#   innings_0_fow_3_batsman_in_id TEXT,
#   innings_0_fow_3_batsman_in_runs TEXT,
#   innings_0_fow_4_runs TEXT,
#   innings_0_fow_4_wickets TEXT,
#   innings_0_fow_4_batsman_out_name TEXT,
#   innings_0_fow_4_batsman_out_id TEXT,
#   innings_0_fow_4_batsman_in_name TEXT,
#   innings_0_fow_4_batsman_in_id TEXT,
#   innings_0_fow_4_batsman_in_runs TEXT,
#   innings_0_fow_5_runs TEXT,
#   innings_0_fow_5_wickets TEXT,
#   innings_0_fow_5_batsman_out_name TEXT,
#   innings_0_fow_5_batsman_out_id TEXT,
#   innings_0_fow_5_batsman_in_name TEXT,
#   innings_0_fow_5_batsman_in_id TEXT,
#   innings_0_fow_5_batsman_in_runs TEXT,
#   innings_0_fow_6_runs TEXT,
#   innings_0_fow_6_wickets TEXT,
#   innings_0_fow_6_batsman_out_name TEXT,
#   innings_0_fow_6_batsman_out_id TEXT,
#   innings_0_fow_6_batsman_in_name TEXT,
#   innings_0_fow_6_batsman_in_id TEXT,
#   innings_0_fow_6_batsman_in_runs TEXT,
#   innings_0_fow_7_runs TEXT,
#   innings_0_fow_7_wickets TEXT,
#   innings_0_fow_7_batsman_out_name TEXT,
#   innings_0_fow_7_batsman_out_id TEXT,
#   innings_0_fow_7_batsman_in_name TEXT,
#   innings_0_fow_7_batsman_in_id TEXT,
#   innings_0_fow_7_batsman_in_runs TEXT,
#   innings_0_fow_8_runs TEXT,
#   innings_0_fow_8_wickets TEXT,
#   innings_0_fow_8_batsman_out_name TEXT,
#   innings_0_fow_8_batsman_out_id TEXT,
#   innings_0_fow_8_batsman_in_name TEXT,
#   innings_0_fow_8_batsman_in_id TEXT,
#   innings_0_fow_8_batsman_in_runs TEXT,
#   innings_0_fow_9_runs TEXT,
#   innings_0_fow_9_wickets TEXT,
#   innings_0_fow_9_batsman_out_name TEXT,
#   innings_0_fow_9_batsman_out_id TEXT,
#   innings_0_fow_9_batsman_in_name TEXT,
#   innings_0_fow_9_batsman_in_id TEXT,
#   innings_0_fow_9_batsman_in_runs TEXT,
#   innings_1_fow_0_runs TEXT,
#   innings_1_fow_0_wickets TEXT,
#   innings_1_fow_0_batsman_out_name TEXT,
#   innings_1_fow_0_batsman_out_id TEXT,
#   innings_1_fow_0_batsman_in_name TEXT,
#   innings_1_fow_0_batsman_in_id TEXT,
#   innings_1_fow_0_batsman_in_runs TEXT,
#   innings_1_fow_1_runs TEXT,
#   innings_1_fow_1_wickets TEXT,
#   innings_1_fow_1_batsman_out_name TEXT,
#   innings_1_fow_1_batsman_out_id TEXT,
#   innings_1_fow_1_batsman_in_name TEXT,
#   innings_1_fow_1_batsman_in_id TEXT,
#   innings_1_fow_1_batsman_in_runs TEXT,
#   innings_1_fow_2_runs TEXT,
#   innings_1_fow_2_wickets TEXT,
#   innings_1_fow_2_batsman_out_name TEXT,
#   innings_1_fow_2_batsman_out_id TEXT,
#   innings_1_fow_2_batsman_in_name TEXT,
#   innings_1_fow_2_batsman_in_id TEXT,
#   innings_1_fow_2_batsman_in_runs TEXT,
#   innings_1_fow_3_runs TEXT,
#   innings_1_fow_3_wickets TEXT,
#   innings_1_fow_3_batsman_out_name TEXT,
#   innings_1_fow_3_batsman_out_id TEXT,
#   innings_1_fow_3_batsman_in_name TEXT,
#   innings_1_fow_3_batsman_in_id TEXT,
#   innings_1_fow_3_batsman_in_runs TEXT,
#   innings_1_fow_4_runs TEXT,
#   innings_1_fow_4_wickets TEXT,
#   innings_1_fow_4_batsman_out_name TEXT,
#   innings_1_fow_4_batsman_out_id TEXT,
#   innings_1_fow_4_batsman_in_name TEXT,
#   innings_1_fow_4_batsman_in_id TEXT,
#   innings_1_fow_4_batsman_in_runs TEXT,
#   innings_1_fow_5_runs TEXT,
#   innings_1_fow_5_wickets TEXT,
#   innings_1_fow_5_batsman_out_name TEXT,
#   innings_1_fow_5_batsman_out_id TEXT,
#   innings_1_fow_5_batsman_in_name TEXT,
#   innings_1_fow_5_batsman_in_id TEXT,
#   innings_1_fow_5_batsman_in_runs TEXT,
#   innings_1_fow_6_runs TEXT,
#   innings_1_fow_6_wickets TEXT,
#   innings_1_fow_6_batsman_out_name TEXT,
#   innings_1_fow_6_batsman_out_id TEXT,
#   innings_1_fow_6_batsman_in_name TEXT,
#   innings_1_fow_6_batsman_in_id TEXT,
#   innings_1_fow_6_batsman_in_runs TEXT,
#   innings_1_fow_7_runs TEXT,
#   innings_1_fow_7_wickets TEXT,
#   innings_1_fow_7_batsman_out_name TEXT,
#   innings_1_fow_7_batsman_out_id TEXT,
#   innings_1_fow_7_batsman_in_name TEXT,
#   innings_1_fow_7_batsman_in_id TEXT,
#   innings_1_fow_7_batsman_in_runs TEXT,
#   innings_1_fow_8_runs TEXT,
#   innings_1_fow_8_wickets TEXT,
#   innings_1_fow_8_batsman_out_name TEXT,
#   innings_1_fow_8_batsman_out_id TEXT,
#   innings_1_fow_8_batsman_in_name TEXT,
#   innings_1_fow_8_batsman_in_id TEXT,
#   innings_1_fow_8_batsman_in_runs TEXT,
#   innings_1_fow_9_runs TEXT,
#   innings_1_fow_9_wickets TEXT,
#   innings_1_fow_9_batsman_out_name TEXT,
#   innings_1_fow_9_batsman_out_id TEXT,
#   innings_1_fow_9_batsman_in_name TEXT,
#   innings_1_fow_9_batsman_in_id TEXT,
#   innings_1_fow_9_batsman_in_runs TEXT,
#   innings_0_bowl_0_bowler_name TEXT,
#   innings_0_bowl_0_bowler_id TEXT,
#   innings_0_bowl_0_overs TEXT,
#   innings_0_bowl_0_maidens TEXT,
#   innings_0_bowl_0_runs TEXT,
#   innings_0_bowl_0_wides TEXT,
#   innings_0_bowl_0_wickets TEXT,
#   innings_0_bowl_0_no_balls TEXT,
#   innings_0_bowl_1_bowler_name TEXT,
#   innings_0_bowl_1_bowler_id TEXT,
#   innings_0_bowl_1_overs TEXT,
#   innings_0_bowl_1_maidens TEXT,
#   innings_0_bowl_1_runs TEXT,
#   innings_0_bowl_1_wides TEXT,
#   innings_0_bowl_1_wickets TEXT,
#   innings_0_bowl_1_no_balls TEXT,
#   innings_0_bowl_2_bowler_name TEXT,
#   innings_0_bowl_2_bowler_id TEXT,
#   innings_0_bowl_2_overs TEXT,
#   innings_0_bowl_2_maidens TEXT,
#   innings_0_bowl_2_runs TEXT,
#   innings_0_bowl_2_wides TEXT,
#   innings_0_bowl_2_wickets TEXT,
#   innings_0_bowl_2_no_balls TEXT,
#   innings_0_bowl_3_bowler_name TEXT,
#   innings_0_bowl_3_bowler_id TEXT,
#   innings_0_bowl_3_overs TEXT,
#   innings_0_bowl_3_maidens TEXT,
#   innings_0_bowl_3_runs TEXT,
#   innings_0_bowl_3_wides TEXT,
#   innings_0_bowl_3_wickets TEXT,
#   innings_0_bowl_3_no_balls TEXT,
#   innings_0_bowl_4_bowler_name TEXT,
#   innings_0_bowl_4_bowler_id TEXT,
#   innings_0_bowl_4_overs TEXT,
#   innings_0_bowl_4_maidens TEXT,
#   innings_0_bowl_4_runs TEXT,
#   innings_0_bowl_4_wides TEXT,
#   innings_0_bowl_4_wickets TEXT,
#   innings_0_bowl_4_no_balls TEXT,
#   innings_0_bowl_5_bowler_name TEXT,
#   innings_0_bowl_5_bowler_id TEXT,
#   innings_0_bowl_5_overs TEXT,
#   innings_0_bowl_5_maidens TEXT,
#   innings_0_bowl_5_runs TEXT,
#   innings_0_bowl_5_wides TEXT,
#   innings_0_bowl_5_wickets TEXT,
#   innings_0_bowl_5_no_balls TEXT,
#   innings_0_bowl_6_bowler_name TEXT,
#   innings_0_bowl_6_bowler_id TEXT,
#   innings_0_bowl_6_overs TEXT,
#   innings_0_bowl_6_maidens TEXT,
#   innings_0_bowl_6_runs TEXT,
#   innings_0_bowl_6_wides TEXT,
#   innings_0_bowl_6_wickets TEXT,
#   innings_0_bowl_6_no_balls TEXT,
#   innings_0_bowl_7_bowler_name TEXT,
#   innings_0_bowl_7_bowler_id TEXT,
#   innings_0_bowl_7_overs TEXT,
#   innings_0_bowl_7_maidens TEXT,
#   innings_0_bowl_7_runs TEXT,
#   innings_0_bowl_7_wides TEXT,
#   innings_0_bowl_7_wickets TEXT,
#   innings_0_bowl_7_no_balls TEXT,
#   innings_0_bowl_8_bowler_name TEXT,
#   innings_0_bowl_8_bowler_id TEXT,
#   innings_0_bowl_8_overs TEXT,
#   innings_0_bowl_8_maidens TEXT,
#   innings_0_bowl_8_runs TEXT,
#   innings_0_bowl_8_wides TEXT,
#   innings_0_bowl_8_wickets TEXT,
#   innings_0_bowl_8_no_balls TEXT,
#   innings_1_team_batting_name TEXT,
#   innings_1_team_batting_id TEXT,
#   innings_1_innings_number TEXT,
#   innings_1_extra_byes TEXT,
#   innings_1_extra_leg_byes TEXT,
#   innings_1_extra_wides TEXT,
#   innings_1_extra_no_balls TEXT,
#   innings_1_extra_penalty_runs TEXT,
#   innings_1_penalties_runs_awarded_in_other_innings TEXT,
#   innings_1_total_extras TEXT,
#   innings_1_runs TEXT,
#   innings_1_wickets TEXT,
#   innings_1_overs TEXT,
#   innings_1_balls TEXT,
#   innings_1_declared TEXT,
#   innings_1_forfeited_innings TEXT,
#   innings_1_revised_target_runs TEXT,
#   innings_1_revised_target_overs TEXT,
#   innings_1_revised_target_balls TEXT,
#   innings_1_bat_0_position TEXT,
#   innings_1_bat_0_batsman_name TEXT,
#   innings_1_bat_0_batsman_id TEXT,
#   innings_1_bat_0_how_out TEXT,
#   innings_1_bat_0_fielder_name TEXT,
#   innings_1_bat_0_fielder_id TEXT,
#   innings_1_bat_0_bowler_name TEXT,
#   innings_1_bat_0_bowler_id TEXT,
#   innings_1_bat_0_runs TEXT,
#   innings_1_bat_0_fours TEXT,
#   innings_1_bat_0_sixes TEXT,
#   innings_1_bat_0_balls TEXT,
#   innings_1_bat_1_position TEXT,
#   innings_1_bat_1_batsman_name TEXT,
#   innings_1_bat_1_batsman_id TEXT,
#   innings_1_bat_1_how_out TEXT,
#   innings_1_bat_1_fielder_name TEXT,
#   innings_1_bat_1_fielder_id TEXT,
#   innings_1_bat_1_bowler_name TEXT,
#   innings_1_bat_1_bowler_id TEXT,
#   innings_1_bat_1_runs TEXT,
#   innings_1_bat_1_fours TEXT,
#   innings_1_bat_1_sixes TEXT,
#   innings_1_bat_1_balls TEXT,
#   innings_1_bat_2_position TEXT,
#   innings_1_bat_2_batsman_name TEXT,
#   innings_1_bat_2_batsman_id TEXT,
#   innings_1_bat_2_how_out TEXT,
#   innings_1_bat_2_fielder_name TEXT,
#   innings_1_bat_2_fielder_id TEXT,
#   innings_1_bat_2_bowler_name TEXT,
#   innings_1_bat_2_bowler_id TEXT,
#   innings_1_bat_2_runs TEXT,
#   innings_1_bat_2_fours TEXT,
#   innings_1_bat_2_sixes TEXT,
#   innings_1_bat_2_balls TEXT,
#   innings_1_bat_3_position TEXT,
#   innings_1_bat_3_batsman_name TEXT,
#   innings_1_bat_3_batsman_id TEXT,
#   innings_1_bat_3_how_out TEXT,
#   innings_1_bat_3_fielder_name TEXT,
#   innings_1_bat_3_fielder_id TEXT,
#   innings_1_bat_3_bowler_name TEXT,
#   innings_1_bat_3_bowler_id TEXT,
#   innings_1_bat_3_runs TEXT,
#   innings_1_bat_3_fours TEXT,
#   innings_1_bat_3_sixes TEXT,
#   innings_1_bat_3_balls TEXT,
#   innings_1_bat_4_position TEXT,
#   innings_1_bat_4_batsman_name TEXT,
#   innings_1_bat_4_batsman_id TEXT,
#   innings_1_bat_4_how_out TEXT,
#   innings_1_bat_4_fielder_name TEXT,
#   innings_1_bat_4_fielder_id TEXT,
#   innings_1_bat_4_bowler_name TEXT,
#   innings_1_bat_4_bowler_id TEXT,
#   innings_1_bat_4_runs TEXT,
#   innings_1_bat_4_fours TEXT,
#   innings_1_bat_4_sixes TEXT,
#   innings_1_bat_4_balls TEXT,
#   innings_1_bat_5_position TEXT,
#   innings_1_bat_5_batsman_name TEXT,
#   innings_1_bat_5_batsman_id TEXT,
#   innings_1_bat_5_how_out TEXT,
#   innings_1_bat_5_fielder_name TEXT,
#   innings_1_bat_5_fielder_id TEXT,
#   innings_1_bat_5_bowler_name TEXT,
#   innings_1_bat_5_bowler_id TEXT,
#   innings_1_bat_5_runs TEXT,
#   innings_1_bat_5_fours TEXT,
#   innings_1_bat_5_sixes TEXT,
#   innings_1_bat_5_balls TEXT,
#   innings_1_bat_6_position TEXT,
#   innings_1_bat_6_batsman_name TEXT,
#   innings_1_bat_6_batsman_id TEXT,
#   innings_1_bat_6_how_out TEXT,
#   innings_1_bat_6_fielder_name TEXT,
#   innings_1_bat_6_fielder_id TEXT,
#   innings_1_bat_6_bowler_name TEXT,
#   innings_1_bat_6_bowler_id TEXT,
#   innings_1_bat_6_runs TEXT,
#   innings_1_bat_6_fours TEXT,
#   innings_1_bat_6_sixes TEXT,
#   innings_1_bat_6_balls TEXT,
#   innings_1_bat_7_position TEXT,
#   innings_1_bat_7_batsman_name TEXT,
#   innings_1_bat_7_batsman_id TEXT,
#   innings_1_bat_7_how_out TEXT,
#   innings_1_bat_7_fielder_name TEXT,
#   innings_1_bat_7_fielder_id TEXT,
#   innings_1_bat_7_bowler_name TEXT,
#   innings_1_bat_7_bowler_id TEXT,
#   innings_1_bat_7_runs TEXT,
#   innings_1_bat_7_fours TEXT,
#   innings_1_bat_7_sixes TEXT,
#   innings_1_bat_7_balls TEXT,
#   innings_1_bat_8_position TEXT,
#   innings_1_bat_8_batsman_name TEXT,
#   innings_1_bat_8_batsman_id TEXT,
#   innings_1_bat_8_how_out TEXT,
#   innings_1_bat_8_fielder_name TEXT,
#   innings_1_bat_8_fielder_id TEXT,
#   innings_1_bat_8_bowler_name TEXT,
#   innings_1_bat_8_bowler_id TEXT,
#   innings_1_bat_8_runs TEXT,
#   innings_1_bat_8_fours TEXT,
#   innings_1_bat_8_sixes TEXT,
#   innings_1_bat_8_balls TEXT,
#   innings_1_bat_9_position TEXT,
#   innings_1_bat_9_batsman_name TEXT,
#   innings_1_bat_9_batsman_id TEXT,
#   innings_1_bat_9_how_out TEXT,
#   innings_1_bat_9_fielder_name TEXT,
#   innings_1_bat_9_fielder_id TEXT,
#   innings_1_bat_9_bowler_name TEXT,
#   innings_1_bat_9_bowler_id TEXT,
#   innings_1_bat_9_runs TEXT,
#   innings_1_bat_9_fours TEXT,
#   innings_1_bat_9_sixes TEXT,
#   innings_1_bat_9_balls TEXT,
#   innings_1_bat_10_position TEXT,
#   innings_1_bat_10_batsman_name TEXT,
#   innings_1_bat_10_batsman_id TEXT,
#   innings_1_bat_10_how_out TEXT,
#   innings_1_bat_10_fielder_name TEXT,
#   innings_1_bat_10_fielder_id TEXT,
#   innings_1_bat_10_bowler_name TEXT,
#   innings_1_bat_10_bowler_id TEXT,
#   innings_1_bat_10_runs TEXT,
#   innings_1_bat_10_fours TEXT,
#   innings_1_bat_10_sixes TEXT,
#   innings_1_bat_10_balls TEXT,
#   innings_1_bowl_0_bowler_name TEXT,
#   innings_1_bowl_0_bowler_id TEXT,
#   innings_1_bowl_0_overs TEXT,
#   innings_1_bowl_0_maidens TEXT,
#   innings_1_bowl_0_runs TEXT,
#   innings_1_bowl_0_wides TEXT,
#   innings_1_bowl_0_wickets TEXT,
#   innings_1_bowl_0_no_balls TEXT,
#   innings_1_bowl_1_bowler_name TEXT,
#   innings_1_bowl_1_bowler_id TEXT,
#   innings_1_bowl_1_overs TEXT,
#   innings_1_bowl_1_maidens TEXT,
#   innings_1_bowl_1_runs TEXT,
#   innings_1_bowl_1_wides TEXT,
#   innings_1_bowl_1_wickets TEXT,
#   innings_1_bowl_1_no_balls TEXT,
#   innings_1_bowl_2_bowler_name TEXT,
#   innings_1_bowl_2_bowler_id TEXT,
#   innings_1_bowl_2_overs TEXT,
#   innings_1_bowl_2_maidens TEXT,
#   innings_1_bowl_2_runs TEXT,
#   innings_1_bowl_2_wides TEXT,
#   innings_1_bowl_2_wickets TEXT,
#   innings_1_bowl_2_no_balls TEXT,
#   innings_1_bowl_3_bowler_name TEXT,
#   innings_1_bowl_3_bowler_id TEXT,
#   innings_1_bowl_3_overs TEXT,
#   innings_1_bowl_3_maidens TEXT,
#   innings_1_bowl_3_runs TEXT,
#   innings_1_bowl_3_wides TEXT,
#   innings_1_bowl_3_wickets TEXT,
#   innings_1_bowl_3_no_balls TEXT,
#   innings_1_bowl_4_bowler_name TEXT,
#   innings_1_bowl_4_bowler_id TEXT,
#   innings_1_bowl_4_overs TEXT,
#   innings_1_bowl_4_maidens TEXT,
#   innings_1_bowl_4_runs TEXT,
#   innings_1_bowl_4_wides TEXT,
#   innings_1_bowl_4_wickets TEXT,
#   innings_1_bowl_4_no_balls TEXT,
#   innings_1_bowl_5_bowler_name TEXT,
#   innings_1_bowl_5_bowler_id TEXT,
#   innings_1_bowl_5_overs TEXT,
#   innings_1_bowl_5_maidens TEXT,
#   innings_1_bowl_5_runs TEXT,
#   innings_1_bowl_5_wides TEXT,
#   innings_1_bowl_5_wickets TEXT,
#   innings_1_bowl_5_no_balls TEXT,
#   innings_1_bowl_6_bowler_name TEXT,
#   innings_1_bowl_6_bowler_id TEXT,
#   innings_1_bowl_6_overs TEXT,
#   innings_1_bowl_6_maidens TEXT,
#   innings_1_bowl_6_runs TEXT,
#   innings_1_bowl_6_wides TEXT,
#   innings_1_bowl_6_wickets TEXT,
#   innings_1_bowl_6_no_balls TEXT,
#   innings_1_bowl_7_bowler_name TEXT,
#   innings_1_bowl_7_bowler_id TEXT,
#   innings_1_bowl_7_overs TEXT,
#   innings_1_bowl_7_maidens TEXT,
#   innings_1_bowl_7_runs TEXT,
#   innings_1_bowl_7_wides TEXT,
#   innings_1_bowl_7_wickets TEXT,
#   innings_1_bowl_7_no_balls TEXT,
#   innings_1_bowl_8_bowler_name TEXT,
#   innings_1_bowl_8_bowler_id TEXT,
#   innings_1_bowl_8_overs TEXT,
#   innings_1_bowl_8_maidens TEXT,
#   innings_1_bowl_8_runs TEXT,
#   innings_1_bowl_8_wides TEXT,
#   innings_1_bowl_8_wickets TEXT,
#   innings_1_bowl_8_no_balls TEXT
# )
# """
# #

# Connect to Turso database
# conn = libsql.connect(database='colchestercavs.db', sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
# cursor = conn.cursor()

# curr = sqlite3.connect('cavsdatabase.db')
# cursor = curr.cursor()

# cursor.execute('DROP TABLE IF EXISTS match_details')

# cursor.execute(competition_teams)
# cursor.execute(fixtures)
# cursor.execute(players)
# cursor.execute(result_summary)
# cursor.execute(teams)
# conn.commit()

# curr.commit()
# curr.close()