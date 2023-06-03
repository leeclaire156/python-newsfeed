# getenv() function is part of Python's built-in os module
# returns the value of the environment variable key (in this case, we specified we want the value of the 'DB_URL' key) if it exists otherwise returns the default value.
from os import getenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
# dotenv works for local development, load_dotenv() reads the file provided as a file path
from dotenv import load_dotenv

# load_dotenv() will set the environment variables from .env and we access with os module
load_dotenv()


url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password=getenv('DB_PASSWORD'),
    host="localhost",
    database="python_news_db",
)

# Below code connects to database using env variable

# The engine variable manages the overall connection to the database.
# In production, DB_URL will be a proper environment variable
engine = create_engine(url_object, echo=True, pool_size=20, max_overflow=0)
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
Session = sessionmaker(bind=engine)
# The Base class variable helps us map the models to real MySQL tables.
Base = declarative_base()