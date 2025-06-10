from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engin = create_engine(SQLALCHEMY_DATABASE_URL)
SessinLocal = sessionmaker(bind=engin, autoflush=False, expire_on_commit=False)
Base = declarative_base()


def get_db():
    db = SessinLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", 
#                             password="Cfytr1984", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sussesfyll")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
