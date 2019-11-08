import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'

app=Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY','freedom')
app.config['SQLALCHEMY_DATABASE_URI']=prefix+os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
login_manager=LoginManager(app)

from watchlist.models import User
@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user

login_manager.login_view='login'
login_manager.login_message='请登录！'

@app.context_processor
def show_user():
    user=User.query.first()
    return dict(user=user)

from watchlist.models import Movie
@app.context_processor
def show_movies():
    movies=Movie.query.all()
    return dict(movies=movies)

from watchlist import views,errrors,commands
