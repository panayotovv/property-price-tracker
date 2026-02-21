from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres-user:password@localhost:5432/scraper_db", echo=True)
SessionLocal = sessionmaker(bind=engine)