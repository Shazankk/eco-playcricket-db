import os
import sqlite3
from dotenv import load_dotenv
import requests
from routes.initdb import fixtures as fixturesql

def fetch_fixtures():
    os.environ.pop('API_TOKEN', None)
    os.environ.pop('SITE_ID', None)
    os.environ.pop('INCLUDE_UNPUBLISHED', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')
    siteId = os.getenv('SITE_ID')
    include_unpublished = os.getenv('INCLUDE_UNPUBLISHED', 'no')
    season = 2025

    apiUrl = f"http://play-cricket.com/api/v2/matches.json"

    params = {
        'api_token': apiToken,
        'site_id': siteId,
        'include_unpublished': 'yes' if include_unpublished == 'yes' else 'no',
        'season': season,
    }

    try:
        response = requests.get(apiUrl, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    if response.status_code == 200:
        matches = response.json().get('matches', [])
        
        # Connect to SQLite database
        with sqlite3.connect('cavsdatabase.db') as conn:
            cursor = conn.cursor()
            
            # Create table schema
            cursor.execute(fixturesql)
            
            insert_data = []
            update_data = []
            
            for match in matches:
                cursor.execute('SELECT * FROM fixtures WHERE id = ?', (match['id'],))
                existing_record = cursor.fetchone()
                
                if existing_record is None:
                    insert_data.append(tuple(match.values()))
                else:
                    existing_data = dict(zip([column[0] for column in cursor.description], existing_record))
                    if existing_data != match:
                        update_data.append(tuple(match.values()) + (match['id'],))
            
            # Batch insert
            if insert_data:
                columns = ', '.join(matches[0].keys())
                placeholders = ', '.join('?' * len(matches[0]))
                sql_insert = f'INSERT INTO fixtures ({columns}) VALUES ({placeholders})'
                cursor.executemany(sql_insert, insert_data)
            
            # Batch update
            if update_data:
                update_placeholders = ', '.join([f"{col}=?" for col in matches[0].keys()])
                sql_update = f'UPDATE fixtures SET {update_placeholders} WHERE id=?'
                cursor.executemany(sql_update, update_data)
            
            # Commit the transaction
            conn.commit()
        
        print("Fixtures data saved to database.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)