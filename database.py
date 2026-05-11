import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the URL from Render's dashboard
url = os.getenv("DATABASE_URL")

# 2. Safety Check: If Render hasn't loaded the variable yet, don't crash
if not url:
    raise ValueError("No DATABASE_URL found in environment variables")

# 3. Standardize the prefix
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

# 4. Create engine with SSL requirements for Supabase
engine = create_engine(
    url,
    connect_args={"sslmode": "require"}, # Required for many cloud providers
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
