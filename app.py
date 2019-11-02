import os,click

from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

from models.movie import Movie




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    """初始化数据库。"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('数据库初始化完毕。')

@app.cli.command()
def forge():
    """生成数据"""
    db.create_all()
    name='meiyujack'
    movies=[
        {'title':'龙猫','year':'1988'},
        {'title':'死亡诗社','year':'1989'},
        {'title':'完美的世界','year':'1993'},
        {'title':'这个杀手不太冷','year':'1994'},
        {'title':'麻将','year':'1996'},
        {'title':'燕尾蝶','year':'1996'},
        {'title':'喜剧之王','year':'1999'},
        {'title':'机器人总动员','year':'2008'},
    ]

    user=User(name=name)
    db.session.add(user)
    for m in movies:
        movie=Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('完成。')

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))

class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    year=db.Column(db.String(4))

    def __repr__(self):
        return '<Movie {}>'.format(self.title)

@app.route('/')
def index():
    user=User.query.first()
    movies=Movie.query.all()
    # movies=[
    # Movie('龙猫','1988'),Movie('死亡诗社','1989'),Movie('完美的世界','1993'),
    # Movie('这个杀手不太冷','1994'),Movie('麻将','1996'),Movie('燕尾蝶','1996'),
    # Movie('喜剧之王','1999'),Movie('机器人总动员','2008')
    # ]
    return render_template('index.html',user=user,movies=movies)

@app.route('/home')
def hello():
    return '欢迎来到我的电影菜单！'+'<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User:{} page '.format(name)

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name='jack'))
    print(url_for('user_page',name='梅'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=2))
    return 'test... '
