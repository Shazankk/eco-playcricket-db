import time
import logging
from fixtures import fetch_fixtures
from match_details import insert_match_data
from players import fetch_players
from result_summary import fetch_result_summary
from club_teams import fetch_teams
from match_details import insert_match_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SLEEP_TIME = 3
def main() -> None:
    try:
        logging.info("Fetching fixtures...")
        fetch_fixtures()
        logging.info("Fixtures fetched and saved to database.")
        time.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching fixtures: {e}")

    try:
        logging.info("Fetching players...")
        fetch_players()
        logging.info("Players fetched and saved to database.")
        time.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching players: {e}")

    try:
        logging.info("Fetching result summary...")
        fetch_result_summary()
        logging.info("Result summary fetched and saved to database.")
        time.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching result summary: {e}")

    try:
        logging.info("Fetching teams...")
        fetch_teams()
        logging.info("Teams fetched and saved to database.")
        time.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching teams: {e}")

    try:
        logging.info("Fetching match details...")
        insert_match_data()
        logging.info("Match details fetched and saved to database.")
        time.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching match details: {e}")

if __name__ == "__main__":
    main()