import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Load local .env if it exists (for local testing)
load_dotenv()

# 2. Get the URL from Render (Cloud) or .env (Local)
# On Render, this will find the "DATABASE_URL" you added to the Environment tab
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. If Render gives 'postgres://', change it to 'postgresql://' for SQLAlchemy
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Create the engine with SSL required (as per Supabase docs)
# pool_pre_ping=True helps keep the connection alive in India/Singapore
engine = create_engine(
    DATABASE_URL, 
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
