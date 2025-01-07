import os
import sqlite3
from dotenv import load_dotenv
import requests
from routes.initdb import players as playersql

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
        
        # Connect to SQLite database (or create it if it doesn't exist)
        with sqlite3.connect('cavsdatabase.db') as conn:
            cursor = conn.cursor()
            
            # Create table schema
            cursor.execute(playersql)
            
            insert_data = []
            update_data = []
            
            for player in players:
                cursor.execute('SELECT * FROM players WHERE member_id = ?', (player['member_id'],))
                existing_record = cursor.fetchone()
                
                if existing_record is None:
                    insert_data.append((player['member_id'], player['name']))
                else:
                    existing_data = dict(zip([column[0] for column in cursor.description], existing_record))
                    if existing_data != player:
                        update_data.append((player['name'], player['member_id']))
            
            # Batch insert
            if insert_data:
                sql_insert = 'INSERT INTO players (member_id, name) VALUES (?, ?)'
                cursor.executemany(sql_insert, insert_data)
            
            # Batch update
            if update_data:
                sql_update = 'UPDATE players SET name = ? WHERE member_id = ?'
                cursor.executemany(sql_update, update_data)
            
            # Commit the transaction
            conn.commit()
        
        print("Players data saved to database.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)