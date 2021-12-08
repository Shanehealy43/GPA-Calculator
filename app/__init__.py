import os

from flask import Flask


'''
each terminal session: 
export FLASK_APP=app
export FLASK_ENV=development
to setup or reset database: flask init-db
to run the server: flask run
'''

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DEBUG=True,
        # a default secret key for sessions for development only
        SECRET_KEY="dev",
        # store the database in the instance folder for development
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    # ensure the instance folder exists, it's where the db will live
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    # start up the database
    from app import db
    db.init_app(app)

    # apply the blueprints to the app
    # tell the app that the routes are in multiple files
    from app import auth, calculator#, calculator
    app.register_blueprint(auth.bp)
    app.register_blueprint(calculator.bp)

    # load the index from blog as the main route page
    # since that rule isn't defined here, need to make the app aware of it
    app.add_url_rule('/', 'index') #THIS LINE

    return app
