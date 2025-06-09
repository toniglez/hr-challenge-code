# Database configuration module
# This module handles database connection setup and session management

import os
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger(__name__)

# Get database URL from environment variable or use SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Fly.io / Heroku Postgres compatibility fix
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    logger.info("Converted postgres:// URL to postgresql:// format")

# Configure database connection parameters
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration
    connect_args = {"check_same_thread": False}
    logger.info("Using SQLite database with check_same_thread=False")

try:
    # Create SQLAlchemy engine with appropriate configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,  # Enable connection health checks
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False           # Set to True to log all SQL queries (development only)
    )
    
    # Add engine event listeners for connection monitoring
    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        logger.debug("Database connection established")
    
    # Create sessionmaker with engine binding
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info(f"Database connection established successfully: {DATABASE_URL.split('://')[0]}")
    
except SQLAlchemyError as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise
