import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This looks for the label "DATABASE_URL" that you created in Render's Environment tab
url = os.getenv("DATABASE_URL")

# Fix for Render/Heroku which sometimes uses 'postgres://'
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

# The engine now uses the 'url' variable
engine = create_engine(
    url, 
    connect_args={"connect_timeout": 10}, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
