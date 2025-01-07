import os
import sqlite3
from dotenv import load_dotenv
import requests
from routes.initdb import competition_teams as competition_teams_sql

def fetch_competition_teams():
    os.environ.pop('API_TOKEN', None)
    os.environ.pop('LEAGUE_ID', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')
    leagueId = os.getenv('LEAGUE_ID')

    if not apiToken:
        print("API token is missing.")
        return

    # Base URL for all teams or league-specific teams
    apiUrl = "http://play-cricket.com/api/v2/competition_teams.json"

    params = {
        'api_token': apiToken,
        'id': leagueId,
    }

    try:
        response = requests.get(apiUrl, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    if response.status_code == 200:
        data = response.json()
        teams = data['competition_teams']

        # Connect to SQLite database (or create it if it doesn't exist)
        with sqlite3.connect('cavsdatabase.db') as conn:
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute(competition_teams_sql)

            for team in teams:
                team['league_id'] = leagueId
                columns = ', '.join(team.keys())
                placeholders = ', '.join('?' * len(team))
                update_placeholders = ', '.join([f"{col}=?" for col in team.keys()])
                
                sql_insert = f'INSERT OR IGNORE INTO competition_teams ({columns}) VALUES ({placeholders})'
                sql_update = f'UPDATE competition_teams SET {update_placeholders} WHERE team_id=?'
                
                cursor.execute(sql_insert, list(team.values()))
                cursor.execute(sql_update, list(team.values()) + [team['team_id']])
            
            # Commit the transaction
            conn.commit()

        print("Competition teams data saved to database.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)