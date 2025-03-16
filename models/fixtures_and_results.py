from database.connection import get_db_connection

class FixturesResults:
    @staticmethod
    async def get_all_fixtures():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fixtures_and_results;")
            fixtures = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in fixtures]
            return result
        except Exception as e:
            print(f"Error fetching fixtures: {e}")
            return []