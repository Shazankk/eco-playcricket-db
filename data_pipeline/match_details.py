from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import libsql_experimental as libsql
import logging

logging.basicConfig(level=logging.DEBUG)

def fetch_match_data():
    os.environ.pop('API_TOKEN', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')

    if not apiToken:
        print("API token is missing.")
        return
    
    apiUrl = "http://play-cricket.com/api/v2/match_detail.json"
    TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
    TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        print("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in the environment variables")
        return

    try:
        print("Connecting to Turso database...")
        conn = libsql.connect(database='colchestercavs.db', sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
        cursor = conn.cursor()
        print("Connected to Turso database.")

        # Fetch all unique match_id from result_summary table
        cursor.execute('SELECT DISTINCT id FROM result_summary')
        match_ids = cursor.fetchall()

        # print("Fetched match IDs:", match_ids)

        for match_id in match_ids:
            params = {
                    'api_token': apiToken,
                    'match_id': match_id[0]
                }

            # Print the constructed API call
            # print(f"API call: {apiUrl}?api_token={apiToken}&match_id={match_id[0]}")

            try:
                response = requests.get(apiUrl, params=params)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to fetch data for match_id {match_id[0]}: {e}")
                continue

            if response.status_code == 200:
                data = response.json()
        
                for match in data["match_details"]:
                    cursor.execute("""
                        INSERT OR IGNORE INTO leagues (league_id, name)
                        VALUES (?, ?)
                        ON CONFLICT (league_id) DO NOTHING
                    """, (match["league_id"], match["league_name"]))
                    
                    # Insert competition
                    cursor.execute("""
                        INSERT OR IGNORE INTO competitions (competition_id, league_id, name, type)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT (competition_id) DO NOTHING
                    """, (match["competition_id"], match["league_id"], 
                        match["competition_name"], match["competition_type"]))
                    
                    # Insert clubs
                    for club_type in ["home_club", "away_club"]:
                        cursor.execute("""
                            INSERT OR IGNORE INTO clubs (club_id, name)
                            VALUES (?, ?)
                            ON CONFLICT (club_id) DO NOTHING
                        """, (match[f"{club_type}_id"], match[f"{club_type}_name"]))
                    
                    # Insert teams
                    for team_type in ["home_team", "away_team"]:
                        club_key = f"{team_type.replace('team', 'club')}_id"
                        cursor.execute("""
                            INSERT OR IGNORE INTO teams (team_id, club_id, name)
                            VALUES (?, ?, ?)
                            ON CONFLICT (team_id) DO NOTHING
                        """, (match[f"{team_type}_id"], 
                                match[club_key], 
                            match[f"{team_type}_name"]))
                    
                    # Insert officials
                    officials = [
                        (match.get("umpire_1_id"), match.get("umpire_1_name"), "Umpire"),
                        (match.get("umpire_2_id"), match.get("umpire_2_name"), "Umpire"),
                        (match.get("scorer_1_id"), match.get("scorer_1_name"), "Scorer"),
                        (match.get("scorer_2_id"), match.get("scorer_2_name"), "Scorer")
                    ]
                    for official_id, name, role in officials:
                        if official_id and official_id.strip():
                            cursor.execute("""
                                INSERT OR IGNORE INTO officials (official_id, name, type)
                                VALUES (?, ?, ?)
                                ON CONFLICT (official_id) DO NOTHING
                            """, (official_id, name, role))
                    
                    # Insert players and match players
                    for team_group in match["players"]:
                        team_type = "home_team" if "home_team" in team_group else "away_team"
                        team_id = match[f"{team_type}_id"]
                        
                        for player in team_group[team_type]:
                            cursor.execute("""
                                INSERT OR IGNORE INTO players (member_id, name)
                                VALUES (?, ?)
                                ON CONFLICT (member_id) DO NOTHING
                            """, (player["player_id"], player["player_name"]))
                            
                            cursor.execute("""
                                INSERT OR IGNORE INTO match_players 
                                (match_id, team_id, player_id, is_captain, is_wicket_keeper, position)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (match["match_id"], team_id, player["player_id"],
                                player["captain"], player["wicket_keeper"], player["position"]))
                    
                    # Insert match result types
                    for result in match["match_result_types"]:
                        result_id = str(result[1]).split("#")[0]
                        team_id = str(result[1]).split("#")[1] if "#" in str(result[1]) else ""
                        # print(result_id, result[0], team_id)
                        cursor.execute("""
                            INSERT OR IGNORE INTO match_result_types (result_type_id, description, team_id)
                            VALUES (?, ?, ?)
                            ON CONFLICT (result_type_id) DO NOTHING
                        """, (result_id, result[0], team_id))
                    
                    # Insert main match record
                    last_updated = (
                        datetime.strptime(match["last_updated"], "%d/%m/%Y").strftime("%Y-%m-%d")
                        if match["last_updated"] else ""
                    )
                    match_date = (
                        datetime.strptime(match["match_date"], "%d/%m/%Y").strftime("%Y-%m-%d")
                        if match["match_date"] else ""
                    )
                    match_time = (
                        datetime.strptime(match["match_time"], "%H:%M").strftime("%H:%M:%S")
                        if match["match_time"] else ""
                    )

                    # Convert numeric string fields to integers where applicable
                    def to_int(val):
                        try:
                            return int(val) if val not in (None, "") else ""
                        except ValueError:
                            return None
                        
                    match_values = (
                        to_int(match["match_id"]),
                        match["status"],
                        match["published"],
                        last_updated,
                        to_int(match["league_id"]),
                        to_int(match["competition_id"]),
                        match["match_type"],
                        match["game_type"],
                        match_date,
                        match_time,
                        match["ground_name"],
                        to_int(match["ground_id"]),
                        to_int(match["home_team_id"]),
                        to_int(match["away_team_id"]),
                        to_int(match.get("umpire_1_id") or ""),
                        to_int(match.get("umpire_2_id") or ""),
                        to_int(match.get("referee_id") or ""),
                        to_int(match.get("scorer_1_id") or ""),
                        to_int(match.get("scorer_2_id") or ""),
                        to_int(match["toss_won_by_team_id"]),
                        match["result"],
                        match["result_description"],
                        match["match_notes"],
                        to_int(match["no_of_innings"]) if match["no_of_innings"] not in (None, "") else ""
                    )

                    cursor.execute("""
                        INSERT OR IGNORE INTO matches (
                            match_id, status, published, last_updated, league_id, competition_id,
                            match_type, game_type, match_date, match_time, ground_name, ground_id,
                            home_team_id, away_team_id, umpire_1_id, umpire_2_id,
                            referee_id, scorer_1_id, scorer_2_id, toss_won_by_team_id,
                            result, result_description, match_notes, no_of_innings
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (match_id) DO NOTHING
                    """, match_values)
                    
                    # Insert points
                    for point in match["points"]:
                        cursor.execute("""
                            INSERT OR IGNORE INTO match_points 
                            (match_id, team_id, game_points, penalty_points, bonus_points_batting, bonus_points_bowling)
                            VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT (match_id, team_id) DO NOTHING
                        """, (
                            match["match_id"],
                            point["team_id"],
                            int(float(point["game_points"])) if point["game_points"] else 0,
                            int(float(point["penalty_points"])) if point["penalty_points"] else 0,
                            int(float(point["bonus_points_batting"])) if point["bonus_points_batting"] else 0,
                            int(float(point["bonus_points_bowling"])) if point["bonus_points_bowling"] else 0
                        ))
                    
                    # Insert innings data
                    for inning in match["innings"]:
                        cursor.execute("""
                            INSERT OR IGNORE INTO innings (
                                match_id, team_batting_id, innings_number, runs, wickets, overs, declared
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            RETURNING inning_id
                        """, (
                            match["match_id"],
                            inning["team_batting_id"],
                            inning["innings_number"],
                            int(inning["runs"]) if inning["runs"] else 0,
                            int(inning["wickets"]) if inning["wickets"] else 0,
                            float(inning["overs"]) if inning["overs"] else 0.0,
                            inning.get("declared", False)
                        ))
                        inning_id = cursor.fetchone()[0]
                        
                        # Insert batting stats
                        for bat in inning["bat"]:
                            cursor.execute("""
                                INSERT OR IGNORE INTO batting_stats (
                                    inning_id, player_id, position, runs, how_out, 
                                    fielder_id, bowler_id, fours, sixes, balls
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                inning_id,
                                bat["batsman_id"],
                                int(bat["position"]),
                                int(bat["runs"]) if bat["runs"] else 0,
                                bat["how_out"],
                                bat["fielder_id"] or "",
                                bat["bowler_id"] or "",
                                int(bat["fours"]) if bat["fours"] else 0,
                                int(bat["sixes"]) if bat["sixes"] else 0,
                                int(bat["balls"]) if bat["balls"] else 0
                            ))
                        
                        # Insert bowling stats
                        for bowl in inning["bowl"]:
                            cursor.execute("""
                                INSERT OR IGNORE INTO bowling_stats (
                                    inning_id, player_id, overs, maidens, runs, wickets, wides, no_balls
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                inning_id,
                                bowl["bowler_id"],
                                float(bowl["overs"]) if bowl["overs"] else 0.0,
                                int(bowl["maidens"]) if bowl["maidens"] else 0,
                                int(bowl["runs"]) if bowl["runs"] else 0,
                                int(bowl["wickets"]) if bowl["wickets"] else 0,
                                int(bowl["wides"]) if bowl["wides"] else 0,
                                int(bowl["no_balls"]) if bowl["no_balls"] else 0
                            ))
                        
                        # Insert fall of wickets
                        for fow in inning["fow"]:
                            cursor.execute("""
                                INSERT OR IGNORE INTO fall_of_wickets (
                                    inning_id, runs, wickets, batsman_out_id, batsman_in_id, batsman_in_runs
                                ) VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                inning_id,
                                int(fow["runs"]),
                                int(fow["wickets"]),
                                fow["batsman_out_id"],
                                fow["batsman_in_id"],
                                int(fow["batsman_in_runs"]) if fow["batsman_in_runs"] else 0
                            ))
                
                conn.commit()
                print("Match details data saved to database.")
    except Exception as e:
        if conn is not None:
            try:
                conn.rollback()
            except Exception as rollback_err:
                print(f"Rollback failed: {rollback_err}")
        print(f"Failed to connect or execute SQL: {e}")