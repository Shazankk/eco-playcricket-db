import os
from dotenv import load_dotenv
import libsql_experimental as libsql

def get_sponsor_data():
    sponsor_name = input("Enter sponsor name (required): ").strip()
    if not sponsor_name:
        print("Sponsor name cannot be empty.")
        exit(1)
    
    website_link = input("Enter website link (required): ").strip()
    if not website_link:
        print("Website link cannot be empty.")
        exit(1)

    logo_url = input("Enter logo URL (required): ").strip()
    if not logo_url:
        print("Logo URL cannot be empty.")
        exit(1)
    
    # If no input is provided, default to "CLUB_WIDE"
    sponsored_entity_type = input("Enter sponsored entity type (PLAYER, TEAM): ").strip().upper()
    if not sponsored_entity_type:
        sponsored_entity_type = "CLUB_WIDE"
    
    # Only require sponsored_entity_id if type is PLAYER or TEAM
    sponsored_entity_id = None
    if sponsored_entity_type in ["PLAYER", "TEAM"]:
        sponsored_entity_id_input = input("Enter sponsored entity ID (integer): ").strip()
        if not sponsored_entity_id_input:
            print("Sponsored entity ID is required for PLAYER or TEAM.")
            exit(1)
        try:
            sponsored_entity_id = int(sponsored_entity_id_input)
        except ValueError:
            print("Sponsored entity ID must be an integer.")
            exit(1)
    
    return {
        "sponsor_name": sponsor_name,
        "website_link": website_link,
        "logo_url": logo_url,
        "sponsored_entity_type": sponsored_entity_type,
        "sponsored_entity_id": sponsored_entity_id
    }

def insert_sponsor(sponsor_data):
    # Load environment variables from .env file
    load_dotenv()
    TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
    TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")
    
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        print("TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in the environment variables.")
        return

    try:
        conn = libsql.connect(database='colchestercavs.db',
                              sync_url=TURSO_DATABASE_URL,
                              auth_token=TURSO_AUTH_TOKEN)
        cursor = conn.cursor()

        # If sponsored_entity_id is None, omit it in the insert so that the default (NULL) is used.
        if sponsor_data["sponsored_entity_id"] is None:
            sql = """INSERT INTO sponsors (sponsor_name, website_link, logo_url, sponsored_entity_type)
                     VALUES (?, ?, ?, ?)"""
            values = (
                sponsor_data["sponsor_name"],
                sponsor_data["website_link"],
                sponsor_data["logo_url"],
                sponsor_data["sponsored_entity_type"]
            )
        else:
            sql = """INSERT INTO sponsors (sponsor_name, website_link, logo_url, sponsored_entity_type, sponsored_entity_id)
                     VALUES (?, ?, ?, ?, ?)"""
            values = (
                sponsor_data["sponsor_name"],
                sponsor_data["website_link"],
                sponsor_data["logo_url"],
                sponsor_data["sponsored_entity_type"],
                sponsor_data["sponsored_entity_id"]
            )

        cursor.execute(sql, values)
        conn.commit()
        print("Sponsor data inserted successfully.")
    except Exception as e:
        print(f"Failed to insert sponsor data: {e}")

def main():
    sponsor_data = get_sponsor_data()
    insert_sponsor(sponsor_data)

if __name__ == "__main__":
    main()