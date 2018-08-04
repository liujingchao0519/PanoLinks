from myapp import db
from myapp.models import Application, User
import csv

def load_application():
    with open('applications.csv') as f:
        mr = csv.reader(f)
        data = list(mr)

        for row in data:
            if row[0] != '':
                new_app = Application()
                new_app.load_data(row)
                db.session.add(new_app)
        db.session.commit()

def load_user():
    with open('user.csv') as f:
        mr = csv.reader(f)
        data = list(mr)

        for row in data:
            if row[0] != '':
                new_user = User()
                new_user.username = row[0]
                new_user.email = row[1]
                db.session.add(new_user)
        db.session.commit()