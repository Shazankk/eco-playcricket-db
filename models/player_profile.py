from database.connection import get_db_connection

class PlayersProfile:
    @staticmethod
    async def get_all_player_profile():
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_profile;")
            stats = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in stats]
            return result
        except Exception as e:
            print(f"Error fetching player profile: {e}")
            return []