from database.connection import get_db_connection

class SponsorsList:
    @staticmethod
    async def get_all_sponsors():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sponsors")
            sponsors = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in sponsors]
            return result
        except Exception as e:
            print(f"Error fetching sponsors: {e}")
            return []