from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from config import BaseConfig
import logging.config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = urandom(24)

db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.questions.views import questions_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(questions_blueprint)

app.config.from_object(BaseConfig)
log_config = app.config['LOGGING_CONFIG']
logging.config.dictConfig(log_config)
logger = logging.getLogger("question_answer_app")
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

@app.before_first_request
def create_tables():
    db.create_all()

