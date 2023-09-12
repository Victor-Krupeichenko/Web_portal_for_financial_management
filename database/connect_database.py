from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.url_database import _URL

engine = create_engine(_URL)

session_maker = sessionmaker(engine, expire_on_commit=False)
