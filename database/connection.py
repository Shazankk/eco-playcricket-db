import os
import logging
from dotenv import load_dotenv
import libsql_experimental as libsql

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables based on NODE_ENV
env = os.getenv('NODE_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
elif env == 'development':
    load_dotenv('.env.development')
    
# Override with local env if exists
load_dotenv('.env.local', override=True)

# Global connection object
_connection = None

def get_db_connection(force_sync=False):
    """Get a database connection, optionally forcing sync with cloud
    
    Args:
        force_sync (bool): If True, force sync with the cloud database
    
    Returns:
        libsql.Connection: Database connection object
    """
    global _connection
    
    # Create a new connection if needed
    if _connection is None:
        db_url = os.getenv('TURSO_DATABASE_URL')
        auth_token = os.getenv('TURSO_AUTH_TOKEN')
        
        if not db_url or not auth_token:
            raise Exception("Database configuration missing")
            
        try:
            _connection = libsql.connect(
                database='colchestercavs.db',
                sync_url=db_url,
                auth_token=auth_token
            )
            logger.info("New database connection established")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise Exception(f"Error connecting to database: {e}")
    
    # Sync with cloud if requested
    if force_sync:
        try:
            _connection.sync()
            logger.info("Database synced with cloud")
        except Exception as e:
            logger.error(f"Error syncing database: {e}")
            # If sync fails, try recreating the connection
            _connection = None
            return get_db_connection(force_sync=False)
    
    return _connection

def refresh_db_connection():
    """Sync the database with cloud to get fresh data
    
    Returns:
        libsql.Connection: A fresh database connection synced with cloud
    """
    conn = get_db_connection(force_sync=True)
    logger.info("Database connection refreshed and synced with cloud")
    return conn

def close_db_connection():
    """Release the database connection
    
    Note: libsql_experimental doesn't need explicit close.
    We just set the connection to None.
    """
    global _connection
    if _connection is not None:
        # No need to call close() as it doesn't exist
        # Just set to None and let Python handle garbage collection
        _connection = None
        logger.info("Database connection released")
        