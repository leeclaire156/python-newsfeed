# getenv() function is part of Python's built-in os module
# returns the value of the environment variable key (in this case, we specified we want the value of the 'DB_URL' key) if it exists otherwise returns the default value.
from os import getenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
# dotenv works for local development, load_dotenv() reads the file provided as a file path
from dotenv import load_dotenv
# used to create global application context
from flask import g

# load_dotenv() will set the environment variables from .env and we access with os module
load_dotenv()

# Below code connects to database using env variable

# The engine variable manages the overall connection to the database.
# In production, DB_URL will be a proper environment variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
Session = sessionmaker(bind=engine)
# The Base class variable helps us map the models to real MySQL tables.
Base = declarative_base()

# Base.metadata... creates database after Flask app is ready and we've called init_db()
def init_db(app):
  Base.metadata.create_all(engine) # Same method from seeds.py

  app.teardown_appcontext(close_db) # Flask will run close_db() together with its built-in teardown_appcontext() method. 

# Returns a new session-connection object
def get_db():
  if 'db' not in g:
    # store current db connection in app context on 'g' object if it isn't already there
    # therefore it can return the connection from the g object instead of creating a new Session instance each time
    g.db = Session()

  return g.db

# Closes connection to the data base in app (global) context
# Prevents infinite number of open session connections and we dont have to add a db.close() to every route
def close_db(e=None):
  # The pop() method attempts to find and remove db from the g object. 
  db = g.pop('db', None)

  # If db exists (that is, db doesn't equal None), then db.close() will end the connection.
  # close_db() function won't run automatically, though. We need to tell Flask to run it whenever a context is destroyed (see def init_db).
  if db is not None:
    db.close()