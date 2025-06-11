from sqlalchemy import create_engine, MetaData
from databases import Database
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não definida no .env")

# Engine e database assíncrono
engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
metadata = MetaData()

# Base para modelos ORM
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
