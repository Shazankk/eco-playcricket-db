import os
import sqlite3
from dotenv import load_dotenv
import requests
from routes.initdb import teams as teamsql

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
        
        # Connect to SQLite database
        with sqlite3.connect('cavsdatabase.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute(teamsql)

            insert_data = []
            update_data = []
            
            for team in teams:
                cursor.execute('SELECT * FROM teams WHERE id = ?', (team['id'],))
                existing_record = cursor.fetchone()
                
                if existing_record is None:
                    insert_data.append(tuple(team.values()))
                else:
                    existing_data = dict(zip([column[0] for column in cursor.description], existing_record))
                    if existing_data != team:
                        update_data.append(tuple(team.values()) + (team['id'],))
            
            # Batch insert
            if insert_data:
                columns = ', '.join(teams[0].keys())
                placeholders = ', '.join('?' * len(teams[0]))
                sql_insert = f'INSERT INTO teams ({columns}) VALUES ({placeholders})'
                cursor.executemany(sql_insert, insert_data)
            
            # Batch update
            if update_data:
                update_placeholders = ', '.join([f"{col}=?" for col in teams[0].keys()])
                sql_update = f'UPDATE teams SET {update_placeholders} WHERE id=?'
                cursor.executemany(sql_update, update_data)
            
            # Commit the transaction
            conn.commit()
        
        print("Teams data saved to database.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)