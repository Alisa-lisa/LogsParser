from application.factories import make_flask_app
import os

environment = os.environ.get('ENVIRONMENT')


app = make_flask_app("log-parser", environment)