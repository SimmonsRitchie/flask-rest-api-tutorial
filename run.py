"""
When deploying program to Heroku or server, use this file as entrypoint

When we run the program locally, we start with app.py. In that case, we meet the __name__ == '__main__'
condition and db is imported before app is run.

However, when we run the app through iWSGI, uWSGI is taking the app variable and running it itself.
That means it is not running the 'app.py' file and therefore our __name__ = '__main__' condition
isn't met, and db isn't imported. We can't move the db import to the top of app.py because it will
create a circular import - creating a big mess.

To get around that, we use this run.py file to import and db. We also alter the uwsgi.ini file
so that it reads 'run:app' rather than 'app:app'

"""
from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    # This creates all the tables in our models unless they exist already
    db.create_all()