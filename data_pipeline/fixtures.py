import os
from dotenv import load_dotenv
import requests
import libsql_experimental as libsql

def fetch_fixtures():
    os.environ.pop('API_TOKEN', None)
    os.environ.pop('SITE_ID', None)
    os.environ.pop('INCLUDE_UNPUBLISHED', None)

    load_dotenv()

    apiToken = os.getenv('API_TOKEN')
    siteId = os.getenv('SITE_ID')
    include_unpublished = os.getenv('INCLUDE_UNPUBLISHED', 'no')
    # This season value will be updated in an outer loop so we can fetch multiple seasons
    seasons = [2021, 2022, 2023, 2024, 2025]

    apiUrl = "http://play-cricket.com/api/v2/matches.json"

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
                'include_unpublished': 'yes' if include_unpublished == 'yes' else 'no',
                'season': season,
            }

            try:
                response = requests.get(apiUrl, params=params)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to fetch data for season {season}: {e}")
                continue

            if response.status_code == 200:
                matches = response.json().get('matches', [])
                print(f"Fetched matches data for season {season}:", matches)

                for match in matches:
                    # Save the season with each fixture so that each season's fixture is stored separately.
                    match['season'] = season

                    columns = ', '.join(match.keys())
                    placeholders = ', '.join('?' * len(match))
                    update_placeholders = ', '.join([f"{col}=?" for col in match.keys()])

                    sql_insert = f'INSERT OR IGNORE INTO fixtures ({columns}) VALUES ({placeholders})'
                    sql_update = f'UPDATE fixtures SET {update_placeholders} WHERE id=? AND season=?'

                    cursor.execute(sql_insert, tuple(match.values()))
                    cursor.execute(sql_update, tuple(match.values()) + (match['id'], match['season']))
            else:
                print(f"Failed to fetch data for season {season}. Status code: {response.status_code}")
                print("Response Content:", response.content)

        # Commit once all seasons are processed
        conn.commit()

        print("Fixtures data saved to database.")
    except Exception as e:
        print(f"Failed to connect or execute SQL: {e}")

# if __name__ == "__main__":
#     fetch_fixtures()