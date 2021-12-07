from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)
#
from werkzeug.exceptions import abort

from app.auth import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("calculator", __name__)

@bp.route("/main")
def main(): # maybe index is name
	db = get_db()
    query = """SELECT firstname, lastname, gpa
            FROM gpa JOIN user ON gpa.user_id = user.id
            ORDER BY created DESC"""
    posts = db.execute(query).fetchall()
    return render_template("calculator/index.html", posts=posts)