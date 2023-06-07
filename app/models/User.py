from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()

# The User class inherits from the Base class from the db package (folder/directory)
class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

  # The validate_email() method uses the assert keyword to check if an email address contains an at-sign character (@).
  @validates('email')
  def validate_email(self, key, email):
    # make sure email address contains @ character
    assert '@' in email
    return email

  @validates('password')
  def validate_password(self, key, password):
    # checks password length; len is short for length
    assert len(password) > 4
    # encrypts password; if the assert doesn't throw an error, returns an encrypted version of the password
    return bcrypt.hashpw(password.encode('utf-8'), salt)
  
  def verify_password(self, password):
    # checkpw() method compares the incoming password (that is, the password parameter) to the one saved on the User object (self.password)
    return bcrypt.checkpw(
      password.encode('utf-8'),
      self.password.encode('utf-8')
  )