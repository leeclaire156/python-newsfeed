from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# POST route that resolves to /api/users
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # attempt creating a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    # saves new user in database
    # use the db.add() method to prep the INSERT statement and the db.commit() method to officially update the database
    db.add(newUser)
    db.commit()
  except:
    #prints error message in terminal
    print(sys.exe_info()[0])
    # If insert failed, rollbacks db connection to prevent crash and sends error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  # clears previous session, adds user id and boolean True as 'logged in' as context for queries/conditional rendering
  # Remember, you can create sessions in Flask only if you've defined a secret key, which was done in app/__init__.py
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  # Otherwise, returns new user's id to the front end
  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204 #A status code of 204 indicates that there is no content.