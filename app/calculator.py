from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
#
from werkzeug.exceptions import abort

from app.auth import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("calculator", __name__)

@bp.route("/main")
@login_required
def main():
	db = get_db()
	gpa = session.get("gpa")
	query = """SELECT firstname, lastname FROM user WHERE id = ?""" #where id = g.user -- look at flask minibloig
	posts = db.execute(query, (g.user["id"],)).fetchall()

	db = get_db()
	query1 = """SELECT * FROM class where user_id = ?"""
	classes = db.execute(query1, (g.user["id"],)).fetchall()
	x = 0
	sum1 = 0
	worthsum = 0
	for each in classes:
	    x += 1
	if x == 0:
	    gpa = None
	else:
	    for each in classes:
	    	if each["length"] == "1-semester":
	    		length1 = 1
	    	else:
	    		length1 = 2
	    	worthsum += each["worth"]
	    	sum1 += length1

	if sum1 > 0:
		gpa = worthsum / sum1
		gpa = round(gpa, 2)
	else:
		gpa = None
	if gpa != None:
		db = get_db()
		query = "INSERT INTO gpa (gpa, user_id) VALUES (?, ?)"
		db.execute(query, (gpa, g.user["id"]))
		db.commit()

	# query = """SELECT firstname, lastname FROM user""" #gpa FROM gpa JOIN user ON gpa.user_id = user.id ORDER BY created DESC
	return render_template("calculator/index.html", posts=posts, gpa=gpa) #, posts=posts (inside parentheses)
@bp.route("/create", methods=("GET", "POST"))
def create():
	if request.method == "POST":
	    classname = request.form["classname"]
	    classtype = request.form["classtype"]
	    length = request.form["length"]
	    grade = request.form["grade"]

	    error = None
	    if not grade:
	    	error = "Grade is required."
	    if not length:
	    	error = "Length is required."
	    if not classtype:
	    	error = "Class type is required."
	    if not classname:
	        error = "Class name is required."

	    if error is not None:
	        flash(error)
	    else:
	    	if grade == "A":
	    		worth = 4
	    	elif grade == "A-":
	    		worth = 3.66
	    	elif grade == "B+":
	    		worth = 3.33
	    	elif grade == "B":
	    		worth = 3
	    	elif grade == "B-":
	    		worth = 2.66
	    	elif grade == "C+":
	    		worth = 2.33
	    	elif grade == "C":
	    		worth = 2
	    	elif grade == "C-":
	    		worth = 1.66
	    	elif grade == "D+":
	    		worth = 1.33
	    	elif grade == "D":
	    		worth = 1
	    	elif grade == "D-":
	    		worth = .66
	    	else:
	    		worth = 0
	    	if classtype == "Honors":
	    		worth += .5
	    	elif classtype == "AP":
	    		worth += 1
	    	if length == "2-semester":
	    		realworth = worth
	    		worth *= 2
	    	else:
	    		realworth = worth
	    	print(worth)
	    	print(realworth)

	    	db = get_db()
	    	query = "INSERT INTO class (classname, classtype, length, grade, user_id, worth, realworth) VALUES (?, ?, ?, ?, ?, ?, ?)"
	    	db.execute(query, (classname, classtype, length, grade, g.user["id"], worth, realworth))
	    	db.commit()

	    	db = get_db()
	    	query1 = """SELECT * FROM class where user_id = ?"""
	    	classes = db.execute(query1, (g.user["id"],)).fetchall()
	    	return redirect(url_for("calculator.create"))

	db = get_db()
	query1 = """SELECT * FROM class where user_id = ?"""
	classes = db.execute(query1, (g.user["id"],)).fetchall()
	return render_template("calculator/create.html", classes=classes)

@bp.route("/delete", methods=("GET", "POST"))
def delete(): #if get
	if request.method == "GET":
		db = get_db()
		query = """SELECT * FROM class where user_id = ?"""
		classes = db.execute(query, (g.user["id"],)).fetchall()
		return render_template("calculator/delete.html", classes=classes) #classes=classes
	else:
		list1 =list(request.form.keys())
		id1 = list1[0]
		db = get_db()
		db.execute("DELETE FROM class WHERE id = ?", (id1,))
		db.commit()
		return redirect(url_for("calculator.delete"))

		# query = """DELETE FROM class where id = ?"""
		# classes = db.execute(query, (id1,)).fetchall()
		# return render_template("calculator/delete.html")
#request.form see which ids are in request.form.keys() 
#if post
	# db = get_db() #I WANNA ADD THIS BUT IDT IT'S RIGHT
	# query = """DELETE * FROM class where id = ?"""
	# classes = db.execute(query, (RIGHT HERE,)).fetchall()
	# db = get_db()
	# return render_template("calculator/create.html")

	# if user_id is None:
 #        g.user = None
 #    else:
 #        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

 #put lines above in main function