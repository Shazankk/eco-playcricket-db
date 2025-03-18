from database.connection import get_db_connection

class PlayersList:
    @staticmethod
    async def get_all_player_stats():
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_batting_stats")
            stats = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in stats]
            return result
        except Exception as e:
            print(f"Error fetching player stats: {e}")
            return []