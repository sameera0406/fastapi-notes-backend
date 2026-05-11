import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. This grabs the single "DATABASE_URL" we set in Render
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Fix the prefix if necessary
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Create the engine using the SSL requirement from your Supabase snippet
# We use 'pool_pre_ping' to make sure the connection hasn't timed out
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
