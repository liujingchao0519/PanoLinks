from myapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from myapp import login
from datetime import datetime
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    application = db.relationship('Application', backref='applicant', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))




class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(140), index=True)
    status = db.Column(db.String(64))
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'))

    sent = db.Column(db.DateTime)
    channel = db.Column(db.String(64))
    invite = db.Column(db.DateTime)
    decision = db.Column(db.DateTime)



    def setUsername(self, username):
        u = User.query.filter_by(username=username).first()
        self.applicant = u



    def load_data(self, data):
        applicant = data[0]
        self.setUsername(applicant)
        self.company = data[1]
        self.status = data[2]
        self.sent = datetime.strptime(data[3], '%x')
        self.channel = data[4]
        if len(data) > 5 and data[5] != '':
            self.invite = datetime.strptime(data[5], '%x')
            self.decision = datetime.strptime(data[6], '%x')





    def __repr__(self):
        return '<Application {}>'.format(self.company)


