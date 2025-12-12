import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from databases import Database

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no .env")

# ❗ O driver deve ser síncrono
# postgresql://... (sem +asyncpg)
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# database async
database = Database(DATABASE_URL)
