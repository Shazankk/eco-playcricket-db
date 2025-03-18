import os
import sqlite3
from dotenv import load_dotenv
import requests
import libsql_experimental as libsql

def fetch_players():
    os.environ.pop('API_TOKEN', None)
    os.environ.pop('SITE_ID', None)
    os.environ.pop('INCLUDE_EVERYONE', None)
    os.environ.pop('INCLUDE_HISTORIC', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')
    siteId = os.getenv('SITE_ID')
    include_everyone = os.getenv('INCLUDE_EVERYONE', 'no')
    include_historic = os.getenv('INCLUDE_HISTORIC', 'no')

    apiUrl = f"http://play-cricket.com/api/v2/sites/{siteId}/players"

    params = {
        'api_token': apiToken,
        'include_everyone': 'yes' if include_everyone == 'yes' else 'no',
        'include_historic': 'yes' if include_historic == 'yes' else 'no',
    }

    try:
        response = requests.get(apiUrl, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    if response.status_code == 200:
        data = response.json()
        players = data['players']

        # Debug: Print fetched data
        # print("Fetched players data:", players)

        # Store values in Turso database
        TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

        if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
            print("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in the environment variables")
            return

        try:
            conn = libsql.connect(database='colchestercavs.db', sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
            cursor = conn.cursor()

            for player in players:
                columns = ', '.join(player.keys())
                placeholders = ', '.join('?' * len(player))
                update_placeholders = ', '.join([f"{col}=?" for col in player.keys()])

                sql_insert = f'INSERT OR IGNORE INTO players ({columns}) VALUES ({placeholders})'
                sql_update = f'UPDATE players SET {update_placeholders} WHERE member_id=?'

                cursor.execute(sql_insert, tuple(player.values()))
                cursor.execute(sql_update, tuple(player.values()) + (player['member_id'],))

            # Commit the transaction
            conn.commit()

            print("Players data saved to database.")
        except Exception as e:
            print(f"Failed to connect or execute SQL: {e}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)