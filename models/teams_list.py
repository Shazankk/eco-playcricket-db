from database.connection import get_db_connection

class TeamsList:
    @staticmethod
    async def get_all_teams():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM club_teams")
            teams = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in teams]
            return result
        except Exception as e:
            print(f"Error fetching teams: {e}")
            return []