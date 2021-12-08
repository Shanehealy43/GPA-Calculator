from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
#
from werkzeug.exceptions import abort

from app.auth import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("calculator", __name__)

@bp.route("/main")
def main():
	db = get_db()

	gpa = session.get("gpa")
	if gpa is None:
		query = """SELECT firstname, lastname FROM user"""
	else:
		query = """SELECT firstname, lastname, gpa FROM user""" #new additions here and lines above


	# query = """SELECT firstname, lastname FROM user""" #gpa FROM gpa JOIN user ON gpa.user_id = user.id ORDER BY created DESC
	posts = db.execute(query).fetchall()
	return render_template("calculator/index.html", posts=posts) #, posts=posts (inside parentheses)
@bp.route("/create")
def create():
	db = get_db()
	return render_template("calculator/create.html")

	# if user_id is None:
 #        g.user = None
 #    else:
 #        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

 #put lines above in main function