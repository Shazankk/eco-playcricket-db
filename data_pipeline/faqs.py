import os
from dotenv import load_dotenv
import libsql_experimental as libsql

def fetch_faqs():
    question = input("Enter FAQ question (required): ").strip()
    if not question:
        print("Question cannot be empty.")
        exit(1)
    
    answer = input("Enter FAQ answer (required): ").strip()
    if not answer:
        print("Answer cannot be empty.")
        exit(1)
    
    return {
        "question": question,
        "answer": answer
    }

def insert_faq(faq_data):
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
        
        sql = "INSERT INTO faqs (question, answer) VALUES (?, ?)"
        values = (faq_data["question"], faq_data["answer"])
        cursor.execute(sql, values)
        conn.commit()
        print("FAQ data inserted successfully.")

    except Exception as e:
        print(f"Failed to insert FAQ data: {e}")

# def main():
#     faq = fetch_faqs()
#     insert_faq(faq)

# if __name__ == "__main__":
#     main()