from myapp import db, create_app
from myapp.models import User, Application

myapp = create_app()

@myapp.shell_context_processor
def make_shell_context():
     return {'db' : db, 'User': User, 'Application': Application}