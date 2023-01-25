from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# "postgresql://<username>:<password>@<ip_addr/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



# Connect to a database to run raw SQL
def connect_to_database(db_host : str, db_name : str, db_user : str, db_pwd : str):
    while True:
        try:
            # None of this hardcoded stuff would normally be here
            conn = psycopg2.connect(host=db_host, database=db_name, \
                user=db_user, password=db_pwd, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connection successful")
            break
        except Exception as error:
            print("Connection to database failed")
            print("Error: ", error)

        time.sleep(2) # Wait a little after an error

