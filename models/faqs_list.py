from database.connection import get_db_connection

class FAQsList:
    @staticmethod
    async def get_all_faqs():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM faqs")
            faqs = cursor.fetchall()
            # Convert tuple results to dictionaries
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in faqs]
            return result
        except Exception as e:
            print(f"Error fetching FAQs: {e}")
            return []