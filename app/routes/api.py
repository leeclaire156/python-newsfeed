from flask import Blueprint, request
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# POST route that resolves to /api/users
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  print(data)

  return ''