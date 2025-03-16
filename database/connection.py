import os
from dotenv import load_dotenv
import libsql_experimental as libsql

# Load environment variables based on NODE_ENV
env = os.getenv('NODE_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
elif env == 'development':
    load_dotenv('.env.development')
    
# Override with local env if exists
load_dotenv('.env.local', override=True)

def get_db_connection():
    db_url = os.getenv('TURSO_DATABASE_URL')
    auth_token = os.getenv('TURSO_AUTH_TOKEN')
    
    if not db_url or not auth_token:
        raise Exception("Database configuration missing")
        
    client = libsql.connect(
        database='colchestercavs.db',
        sync_url=db_url,
        auth_token=auth_token
    )
    return client