from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# POST (create) route for signup that resolves to /api/users
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

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    # if cant find email in db, print error
    print(sys.exc_info()[0])
    return jsonify(message = 'Incorrect credentials'), 400
  
  # if password doesn't match, also print error
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400
  
  # if email is there in db and passwords match, perform the following code to create a session and log them in
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()
  
  try:
    # create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    # db.commit() performs INSERT against the database
    db.commit()
  except:
    print(sys.exc_info()[0])
    # db.rollback() discards the pending commit to db if it fails to prevent app crash
    db.rollback()
    return jsonify(message = 'Comment failed'), 500
  
  # This return runs if everything's ok (as in, the except block didn't run)
  return jsonify(id = newComment.id)

# Remember, PUT route = update in CRUD 
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

# route for creating post
@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

# route for updating posts 
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  db = get_db()
  
  # we find the post, update it, and will recommit it
  # data is a dictionary and uses bracket notation, Post is an object from user class and uses dot notation
  # remember that objects in python can only be made from classes
  try:
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message = 'Post not found'), 404
  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204