
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Create engine using configuration from config.py
engine = create_async_engine(settings.DATABASE_URL, echo=not settings.is_production)

# Create session factory
async_session = sessionmaker(autocommit=False, 
                             autoflush=False, 
                             bind=engine, 
                             class_=AsyncSession,
                             expire_on_commit=False)

# Base class for declarative models
Base = declarative_base()
