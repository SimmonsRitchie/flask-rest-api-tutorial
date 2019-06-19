"""
We start program here for two reasons:
1) If we try to import db.py in app.py we will have a circular import, causing
major problems
2) We can't import on 'if __name__ == '__main__' because when deployed to Heroku
UWSGI ignores this.
"""
from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    # This creates all the tables in our models unless they exist already
    db.create_all()