import logging
from routes.competition_teams import fetch_competition_teams
from routes.fixtures import fetch_fixtures
from routes.match_details_normalised import insert_match_data
from routes.players import fetch_players
from routes.result_summary import fetch_result_summary
from routes.teams import fetch_teams
from routes.match_details_normalised import insert_match_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # try:
    #     logging.info("Fetching competition teams...")
    #     fetch_competition_teams()
    #     logging.info("Competition teams fetched and saved to database.")
    # except Exception as e:
    #     logging.error(f"Error fetching competition teams: {e}")

    try:
        logging.info("Fetching fixtures...")
        fetch_fixtures()
        logging.info("Fixtures fetched and saved to database.")
    except Exception as e:
        logging.error(f"Error fetching fixtures: {e}")

    try:
        logging.info("Fetching players...")
        fetch_players()
        logging.info("Players fetched and saved to database.")
    except Exception as e:
        logging.error(f"Error fetching players: {e}")

    try:
        logging.info("Fetching result summary...")
        fetch_result_summary()
        logging.info("Result summary fetched and saved to database.")
    except Exception as e:
        logging.error(f"Error fetching result summary: {e}")

    # try:
    #     logging.info("Fetching teams...")
    #     fetch_teams()
    #     logging.info("Teams fetched and saved to database.")
    # except Exception as e:
    #     logging.error(f"Error fetching teams: {e}")

    try:
        logging.info("Fetching match details...")
        insert_match_data()
        logging.info("Match details fetched and saved to database.")
    except Exception as e:
        logging.error(f"Error fetching match details: {e}")

if __name__ == "__main__":
    main()