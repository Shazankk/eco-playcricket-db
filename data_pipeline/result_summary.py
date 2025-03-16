import os
from dotenv import load_dotenv
import requests
import libsql_experimental as libsql

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
    seasons = [2024, 2025]

    apiUrl = f"http://play-cricket.com/api/v2/result_summary"

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
        
        # Store values in Turso database
        TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

        if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
            print("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in the environment variables")
            return

        try:
            conn = libsql.connect(database='colchestercavs.db', sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
            cursor = conn.cursor()

            for season in seasons:
                params = {
                    'api_token': apiToken,
                    'site_id': siteId,
                    'league_id': leagueId,
                    'competition_type': competition_type,
                    'season': season,
                }

            for item in flattened_data:
                columns = ', '.join(item.keys())
                placeholders = ', '.join('?' * len(item))
                update_placeholders = ', '.join([f"{col}=?" for col in item.keys()])

                sql_insert = f'INSERT OR IGNORE INTO result_summary ({columns}) VALUES ({placeholders})'
                sql_update = f'UPDATE result_summary SET {update_placeholders} WHERE id=?'

                cursor.execute(sql_insert, tuple(item.values()))
                cursor.execute(sql_update, tuple(item.values()) + (item['id'],))

            # Commit the transaction
            conn.commit()

            print("Result summary data saved to database.")
        except Exception as e:
            print(f"Failed to connect or execute SQL: {e}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response Content:", response.content)