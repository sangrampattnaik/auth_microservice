from curses import echo
from apps.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DB_URI,pool_pre_ping=True)
session = sessionmaker(bind=engine,autocommit=False,autoflush=False)




