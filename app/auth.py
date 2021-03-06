import functools#RESOURCES USED: W3 Schools, Mx. Hansberry
#
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

# every auth route has the prefix below
bp = Blueprint("auth", __name__, url_prefix="/")

@bp.route("/") #main route - sends user to login
def index():
    return redirect(url_for("auth.login"))

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: # if no one is logged in, redirect
            return redirect(url_for("auth.login"))

        return view(**kwargs) # otherwise continue showing the view they asked for

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    # put the user in the g namespace to prevent needing to do SELECT all the time
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the email is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST": #posting it when submitted
        firstname = request.form["firstname"] #need all the following four inputs from the user
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        if not firstname: #need all the inputs or else error will pop up
            error = "First Name is required."
        elif not lastname:
            error = "Last Name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute("INSERT INTO user (firstname, lastname, email, password) VALUES (?, ?, ?, ?)", #insert the user inputs into table.
                    (firstname, lastname, email, generate_password_hash(password))) #encrypt password
                db.commit()
            except db.IntegrityError:
                # The email was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"Email {email} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error) # shows up on the base.html template to show errors

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():

    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST": #when submit button is pressed
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone() #make sure credentials match

        if user is None: #if no users were matched to credentials inputted
            error = "This email does not match an account." 
        elif not check_password_hash(user["password"], password): #if passcode incorrect
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("calculator.main", id=user['id'])) #if there's no errors, then send the user to THEIR home page,

        flash(error)

    return render_template("auth/login.html") #generate output from credentials given


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("auth.login")) #shouldn't it be back to the login page?
# @bp.route("/")

