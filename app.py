import os,click

from flask import Flask,url_for,render_template,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user

from models.movie import Movie

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='freedom'

db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message='请登录！'

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
    click.echo('数据已导入。')

@app.cli.command()
@click.option('--username',prompt=True,help='设置用户名用来登陆')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='设置密码用来登陆')
def admin(username,password):
    """创建用户"""
    db.create_all()

    user=User.query.first()
    if user is not None:
        click.echo('更新用户中......')
        user.username=username
        user.set_password(password)
    else:
        click.echo('创建用户中......')
        user=User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('完成。')

@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        if not username or not password:
            flash('非法输入!')
            return redirect(url_for('login'))

        user=User.query.first()
        if username==user.username and user.validate_password(password):
            login_user(user)
            flash('登陆成功！')
            return redirect(url_for('index'))

        flash('无效用户名或密码。')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('拜拜~')
    return redirect(url_for('index'))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    username=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    year=db.Column(db.String(4))

    def __repr__(self):
        return '<Movie {}>'.format(self.title)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title=request.form.get('title')
        year=request.form.get('year')
        if not title or not year or len(year)!=4 or len(title)>60:
            flash('非法输入！')
            return redirect(url_for('index'))
        movie=Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('已创建！')
        return redirect(url_for('index'))

    return render_template('index.html')
    # movies=Movie.query.all()
    # movies=[
    # Movie('龙猫','1988'),Movie('死亡诗社','1989'),Movie('完美的世界','1993'),
    # Movie('这个杀手不太冷','1994'),Movie('麻将','1996'),Movie('燕尾蝶','1996'),
    # Movie('喜剧之王','1999'),Movie('机器人总动员','2008')
    # ]
    # return render_template('index.html',movies=movies)

@app.route('/add')
@login_required
def add():
    return render_template('form.html')

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie=Movie.query.get_or_404(movie_id)

    if request.method=='POST':
        title=request.form['title']
        year=request.form['year']

        if not title or not year or len(year)!=4 or len(title)>60:
            flash('非法输入！')
            return redirect(url_for('edit',movie_id=movie_id))

        movie.title=title
        movie.year=year
        db.session.commit()
        flash('条目已更新。')
        return redirect(url_for('index'))

    return render_template('edit.html',movie=movie)

@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
@login_required
def delete(movie_id):
    movie=Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('该条目已删除')
    return redirect(url_for('index'))

@app.route('/home')
def hello():
    return '欢迎来到我的电影菜单！'+'<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User:{} page '.format(name)

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method=='POST':
        name=request.form['name']

        if not name or len(name)>20:
            flash('非法输入！')
            return redirect(url_for('settings'))

        current_user.name=name
        db.session.commit()
        flash('设置已更新。')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name='jack'))
    print(url_for('user_page',name='梅'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=2))
    return 'test... '

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.context_processor
def show_user():
    user=User.query.first()
    return dict(user=user)

@app.context_processor
def show_movies():
    movies=Movie.query.all()
    return dict(movies=movies)

@app.route('/ttt')
def ttt():
    return render_template('base.html')
