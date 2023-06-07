from flask import session, redirect
# functools module contains several helper functions that we can use to change other functions
# wraps() is a decorator function like the @bp.route() functions
from functools import wraps

# goal of custom decorator function: redirect a user who isn't logged in (that is, a user for whom no session exists) or to continue on and run the original route function for a user who is logged in
# essentially, it will be our middleware
def login_required(func):
  @wraps(func)
  def wrapped_function(*args, **kwargs):
    # if logged in, call original function with original arguments
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)

    return redirect('/login')
  
  return wrapped_function