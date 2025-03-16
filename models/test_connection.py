import os
import sys
import asyncio

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_db_connection

def test_connection():
    try:
        client = get_db_connection()
        cursor = client.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("Connection is live. Query result:", result)
    except Exception as e:
        print("Connection test failed:", e)

if __name__ == "__main__":
    test_connection()