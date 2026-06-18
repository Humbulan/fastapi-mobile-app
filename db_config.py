import os
from sqlalchemy import create_engine
import pymysql

# MariaDB connection parameters
MYSQL_SOCKET = os.path.expanduser("~/mysql_run/mysql.sock")
MYSQL_USER = 'u0_a336'
MYSQL_DB = 'imperial_nexus'

# Build database URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:@localhost/{MYSQL_DB}?unix_socket={MYSQL_SOCKET}"

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def get_db_connection():
    """Return a raw pymysql connection (for scripts that don't use SQLAlchemy)"""
    return pymysql.connect(
        unix_socket=MYSQL_SOCKET,
        user=MYSQL_USER,
        database=MYSQL_DB,
        autocommit=True
    )
