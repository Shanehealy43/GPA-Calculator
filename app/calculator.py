from flask import (#RESOURCES USED: W3 Schools, Mx. Hansberry
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
#
from werkzeug.exceptions import abort

from app.auth import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("calculator", __name__)

@bp.route("/main") #route for home page
@login_required
def main():
	db = get_db()
	gpa = session.get("gpa")
	query = """SELECT firstname, lastname FROM user WHERE id = ?""" #gets full name of user
	posts = db.execute(query, (g.user["id"],)).fetchall() #saves the command above in a variable "posts"

	db = get_db()
	query1 = """SELECT * FROM class where user_id = ?""" #get everything about each class, as long as it belongs to the user.
	classes = db.execute(query1, (g.user["id"],)).fetchall() #saves command above in variable "classes"
	x = 0 #this var is to make sure there is actually a class in the database, otherwise, the gpa can't be calculated.
	sum1 = 0 #this is the variable that will eventually become the denominator of the gpa --> it's a combination of all the credits
	worthsum = 0 #this variable will be the numerator of the gpa --> it's influenced by the length, type, and grade of a class.
	for each in classes: #for each class in the table "class"
	    x += 1 #add x
	if x == 0: #this is what I was mentioning above... if there's 0 classes, then there's no gpa.
	    gpa = None
	else: #if there are classes
	    for each in classes: # then for each class in the table
	    	if each["length"] == "1-semester": # if the length is a 1-semester class
	    		length1 = 1 #then this variable is 1 - I basically created this var to conver the length into an int.
	    	else: #otherwise, the class is two semesters.
	    		length1 = 2
	    	worthsum += each["worth"] #the numerator is all the classes in the tables value added up.
	    	sum1 += length1 #the denominator just adds up each of the classes credits

	if sum1 > 0: #can only calculate gpa if denom. is > 0 - you'll get an error otherwise.
		gpa = worthsum / sum1 #this is the gpa
		gpa = round(gpa, 2) #round it to the hundredths.
	else:
		gpa = None
	if gpa != None: #if the gpa has a value other than none
		db = get_db()
		query = "INSERT INTO gpa (gpa, user_id) VALUES (?, ?)" #then insert it into the table!
		db.execute(query, (gpa, g.user["id"])) #this puts it through.
		db.commit() #this as well

	# query = """SELECT firstname, lastname FROM user""" #gpa FROM gpa JOIN user ON gpa.user_id = user.id ORDER BY created DESC
	return render_template("calculator/index.html", posts=posts, gpa=gpa) #, posts=posts (inside parentheses)
@bp.route("/create", methods=("GET", "POST"))
def create():
	if request.method == "POST":#if we're submitting stuff
	    classname = request.form["classname"] #this is what the user inputs for the classname, type, etc. Saved into vars.
	    classtype = request.form["classtype"]
	    length = request.form["length"]
	    grade = request.form["grade"]

	    error = None
	    if not grade:
	    	error = "Grade is required."# they all need to be filled out to advance
	    if not length:
	    	error = "Length is required."
	    if not classtype:
	    	error = "Class type is required."
	    if not classname:
	        error = "Class name is required."

	    if error is not None:
	        flash(error)
	    else:
	    	if grade == "A":#so the worth is each classes value. The following 30 lines is how it's calculated
	    		worth = 4 #essentially, every grade down is -.33 to the value. Honors adds .5; AP adds 1.
	    	elif grade == "A-":#A 2-semester class counts twice as much as a 1-semester class
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

	    	db = get_db()
	    	query = "INSERT INTO class (classname, classtype, length, grade, user_id, worth, realworth) VALUES (?, ?, ?, ?, ?, ?, ?)" #insert everything piece of info we got about the class into the table
	    	db.execute(query, (classname, classtype, length, grade, g.user["id"], worth, realworth))
	    	db.commit()

	    	db = get_db()
	    	query1 = """SELECT * FROM class where user_id = ?""" #select everything because we need it to see the classes that already are stored in the db.
	    	classes = db.execute(query1, (g.user["id"],)).fetchall()
	    	return redirect(url_for("calculator.create")) #go back to same page. On html, the new class will be added.

	db = get_db()
	query1 = """SELECT * FROM class where user_id = ?"""#select everything because we need it to see the classes that already are stored in the db.
	classes = db.execute(query1, (g.user["id"],)).fetchall()
	return render_template("calculator/create.html", classes=classes) #generate output.

@bp.route("/delete", methods=("GET", "POST")) #delete page
def delete(): #if get
	if request.method == "GET": #when the page loads
		db = get_db()
		query = """SELECT * FROM class where user_id = ?""" #select everything. Once again, so you can see the classes stored in database.
		classes = db.execute(query, (g.user["id"],)).fetchall()#execute
		return render_template("calculator/delete.html", classes=classes) #generate output.
	else:#if it's a post.
		list1 =list(request.form.keys()) #these next few lines are matching the button pressed to delete to the contents of the table matching the text next to the button
		id1 = list1[0]
		db = get_db()
		db.execute("DELETE FROM class WHERE id = ?", (id1,))
		db.commit()
		return redirect(url_for("calculator.delete"))#still gonna be in the delete file after
