import os
from app import create_app, db
from app.models import *
from app.models_data import load_models_data
from flask_script import Manager, Shell

app = create_app('config')
manager = Manager(app)

with app.app_context():
    # Recreate database
    db.drop_all()
    db.create_all()
    # Load example data for database
    load_models_data()

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()