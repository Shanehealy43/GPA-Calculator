from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)
#
from werkzeug.exceptions import abort

from app.auth import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("calculator", __name__)

# @bp.route("/main")
# def index():
# 	db = get_db()
#     query = """SELECT post.id, title, body, created, author_id, username
#             FROM post JOIN user ON post.author_id = user.id
#             ORDER BY created DESC"""