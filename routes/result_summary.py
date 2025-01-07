import os
import sqlite3
import json
from dotenv import load_dotenv
import requests
from routes.initdb import result_summary as result_summary_sql

def fetch_result_summary():
    os.environ.pop('API_TOKEN', None)
    os.environ.pop('SITE_ID', None)
    os.environ.pop('LEAGUE_ID', None)
    os.environ.pop('COMPETITION_TYPE', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')
    siteId = os.getenv('SITE_ID')
    leagueId = os.getenv('LEAGUE_ID')
    competition_type = os.getenv('COMPETITION_TYPE')
    season = 2024

    apiUrl = f"http://play-cricket.com/api/v2/result_summary"

    params = {
        'api_token': apiToken,
        'site_id': siteId,
        'league_id': leagueId,
        'competition_type': competition_type,
        'season': season,
    }

    try:
        response = requests.get(apiUrl, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    if response.status_code == 200:
        data = response.json()
        result_summary = data['result_summary']
        
        def flatten_json(y):
            out = {}

            def flatten(x, name=''):
                if type(x) is dict:
                    for a in x:
                        flatten(x[a], name + a + '_')
                elif type(x) is list:
                    i = 0
                    for a in x:
                        flatten(a, name + str(i) + '_')
                        i += 1
                else:
                    out[name[:-1]] = x

            flatten(y)
            return out

        flattened_data = [flatten_json(item) for item in result_summary]
        
        # Connect to SQLite database
        with sqlite3.connect('cavsdatabase.db') as conn:
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute(result_summary_sql)
            
            # Prepare batch insert and update
            insert_data = []
            update_data = []
            
            for item in flattened_data:
                cursor.execute('SELECT * FROM result_summary WHERE id = ?', (item['id'],))
                existing_record = cursor.fetchone()
                
                if existing_record is None:
                    insert_data.append(tuple(item.values()))
                else:
                    existing_data = dict(zip([column[0] for column in cursor.description], existing_record))
                    if existing_data != item:
                        update_data.append(tuple(item.values()) + (item['id'],))
            
            # Batch insert
            if insert_data:
                columns = ', '.join(flattened_data[0].keys())
                placeholders = ', '.join('?' * len(flattened_data[0]))
                sql_insert = f'INSERT INTO result_summary ({columns}) VALUES ({placeholders})'
                cursor.executemany(sql_insert, insert_data)
            
            # Batch update
            # if update_data:
            #     update_placeholders = ', '.join([f"{col}=?" for col in flattened_data[0].keys()])
            #     sql_update = f'UPDATE result_summary SET {update_placeholders} WHERE id=?'
            #     cursor.executemany(sql_update, update_data)
            
            # Commit the transaction
            conn.commit()
        
        print("Result summary data saved to database.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)