import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Look for the label "DATABASE_URL" from Render's Environment tab
url = os.getenv("DATABASE_URL")

# 2. Safety check: ensure the URL exists and has the correct prefix
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

# 3. Create the connection engine using the 'url' variable
engine = create_engine(
    url, 
    connect_args={"connect_timeout": 10}, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
