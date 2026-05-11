import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Fix the prefix (Render/Heroku standard)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Create the engine with a timeout to prevent hanging
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"}
    )
    # Test connection immediately on startup
    with engine.connect() as conn:
        print("Successfully connected to Supabase!")
except Exception as e:
    print(f"DATABASE CONNECTION ERROR: {e}")
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
