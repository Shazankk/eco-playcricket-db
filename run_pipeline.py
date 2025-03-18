import asyncio
import logging

from data_pipeline.competition_teams import fetch_competition_teams
from data_pipeline.fixtures import fetch_fixtures
from data_pipeline.players import fetch_players
from data_pipeline.result_summary import fetch_result_summary
from data_pipeline.club_teams import fetch_teams
# from data_pipeline.sponsors import fetch_sponsors
from data_pipeline.match_details import fetch_match_data
# from data_pipeline.faqs import fetch_faqs

SLEEP_TIME = 3  # seconds between pipeline calls

async def run_pipeline():
    try:     
        logging.info("Fetching fixtures...")
        await fetch_fixtures()
        logging.info("Fixtures fetched and saved to database.")
        await asyncio.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching fixtures: {e}")

    try:
        logging.info("Fetching players...")
        await fetch_players()
        logging.info("Players fetched and saved to database.")
        await asyncio.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching players: {e}")

    try:
        logging.info("Fetching result summary...")
        await fetch_result_summary()
        logging.info("Result summary fetched and saved to database.")
        await asyncio.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching result summary: {e}")

    try:
        logging.info("Fetching teams...")
        await fetch_teams()
        logging.info("Teams fetched and saved to database.")
        await asyncio.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching teams: {e}")

    try:
        logging.info("Fetching match details...")
        await fetch_match_data()
        logging.info("Match details fetched and saved to database.")
        await asyncio.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"Error fetching match details: {e}")

    # try:
    #     logging.info("Fetching sponsor details...")
    #     await fetch_sponsors()
    #     logging.info("Sponsor details fetched and saved to database.")
    #     await asyncio.sleep(SLEEP_TIME)
    # except Exception as e:
    #     logging.error(f"Error fetching sponsor details: {e}")

    # try:
    #     logging.info("Fetching FAQ details...")
    #     await fetch_faqs()
    #     logging.info("FAQ details fetched and saved to database.")
    #     await asyncio.sleep(SLEEP_TIME)
    # except Exception as e:
    #     logging.error(f"Error fetching FAQ details: {e}")

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())