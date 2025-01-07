import os
import sqlite3
import json
from dotenv import load_dotenv
import requests
from routes.initdb import match_details as match_details_sql

def fetch_match_details():
    os.environ.pop('API_TOKEN', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')

    if not apiToken:
        print("API token is missing.")
        return

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

    # Base URL
    apiUrl = f"http://play-cricket.com/api/v2/match_detail.json"

    # Connect to SQLite database
    with sqlite3.connect('cavsdatabase.db') as conn:
        cursor = conn.cursor()

        # Fetch all unique match_id from result_summary table
        cursor.execute('SELECT DISTINCT id FROM result_summary')
        match_ids = cursor.fetchall()

        for match_id in match_ids:
            params = {
                'api_token': apiToken,
                'match_id': match_id[0]
            }

            try:
                response = requests.get(apiUrl, params=params)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to fetch data for match_id {match_id[0]}: {e}")
                continue

            if response.status_code == 200:
                data = response.json()
                match_details = data['match_details'][0]

                flattened_data = flatten_json(match_details)

                # Create table with the correct schema
                cursor.execute(match_details_sql)

                # Check if the record exists
                cursor.execute('SELECT * FROM match_details WHERE id = ?', (flattened_data['id'],))
                existing_record = cursor.fetchone()

                if existing_record is None:
                    # Insert new record
                    columns = ', '.join(flattened_data.keys())
                    placeholders = ', '.join('?' * len(flattened_data))
                    sql_insert = f'INSERT INTO match_details ({columns}) VALUES ({placeholders})'
                    cursor.execute(sql_insert, list(flattened_data.values()))
                else:
                    # Update only if data is different
                    existing_data = dict(zip([column[0] for column in cursor.description], existing_record))
                    if existing_data != flattened_data:
                        update_placeholders = ', '.join([f'{key} = ?' for key in flattened_data.keys()])
                        sql_update = f'UPDATE match_details SET {update_placeholders} WHERE id = ?'
                        cursor.execute(sql_update, list(flattened_data.values()) + [flattened_data['id']])

        # Commit the transaction
        conn.commit()

    print("Match details data saved to database.")