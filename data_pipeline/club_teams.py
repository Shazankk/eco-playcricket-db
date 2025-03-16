import os
import sqlite3
from dotenv import load_dotenv
import requests
import libsql_experimental as libsql

def fetch_teams():
    os.environ.pop('API_TOKEN', None)
    os.environ.pop('SITE_ID', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')
    siteId = os.getenv('SITE_ID')

    if not apiToken:
        print("API token is missing.")
        exit(1)

    # Base URL for all teams or site-specific teams
    apiUrl = f"https://www.play-cricket.com/api/v2/sites/{siteId}/teams.json" if siteId else "https://www.play-cricket.com/api/v2/teams.json"

    params = {
        'api_token': apiToken
    }

    try:
        response = requests.get(apiUrl, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        exit(1)

    if response.status_code == 200:
        teams = response.json().get('teams', [])
        
        # Debug: Print fetched data
        print("Fetched teams data:", teams)

        # Store values in Turso database
        TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

        if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
            print("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in the environment variables")
            return

        try:
            conn = libsql.connect(database='colchestercavs.db', sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
            cursor = conn.cursor()

            for team in teams:
                columns = ', '.join(team.keys())
                placeholders = ', '.join('?' * len(team))
                update_placeholders = ', '.join([f"{col}=?" for col in team.keys()])

                sql_insert = f'INSERT OR IGNORE INTO club_teams ({columns}) VALUES ({placeholders})'
                sql_update = f'UPDATE club_teams SET {update_placeholders} WHERE id=?'

                cursor.execute(sql_insert, tuple(team.values()))
                cursor.execute(sql_update, tuple(team.values()) + (team['id'],))

            # Commit the transaction
            conn.commit()

            print("Teams data saved to database.")
        except Exception as e:
            print(f"Failed to connect or execute SQL: {e}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)