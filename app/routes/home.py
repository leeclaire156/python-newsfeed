from flask import Blueprint, render_template
from app.models import Post
from app.db import get_db
# Blueprint() lets us consolidate routes onto a single 'bp' object that the parent app can register later.
# This corresponds to using the Router middleware of Express.js
bp = Blueprint('home', __name__, url_prefix='/')
# @bp.route() decorator before the function turns it into a route.
# render_template() function responds with a template instead of a string.
@bp.route('/')
def index():
  # get all posts
  # get_db() function returns a session connection that's tied to this route's context
  db = get_db()
  # We use query() method on the connection object (db) to query the Post model and save all that in the posts variable
  # Multiline query below, single line version: posts = db.query(Post).order_by(Post.created_at.desc()).all()
  # MUST use parentheses in python for multiline queries, unlike in JS
  posts = (
    db
      .query(Post)
      .order_by(Post.created_at.desc())
      .all()
  )
  
  # returning homepage WITH the posts
  return render_template(
  'homepage.html',
  posts=posts
)

@bp.route('/login')
def login():
  return render_template('login.html')

@bp.route('/post/<id>')
def single(id):
  # get single post by id
  db = get_db()
  # filter() method serves as SQL's "WHERE" clause and is used with .one() instead of .all() to get a single post
  post = db.query(Post).filter(Post.id == id).one()

  # render single post template
  return render_template(
    'single-post.html',
    post=post
  )