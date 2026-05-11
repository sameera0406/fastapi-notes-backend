import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual string from Step 1
SQLALCHEMY_DATABASE_URL = os.getenv("postgresql://postgres:RaghaSameera%401546@db.ldapzmifzmpcopwsnihx.supabase.co:5432/postgres")
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
# The engine is the actual connection to Supabase
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"connect_timeout": 10}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
