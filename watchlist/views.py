from flask import Flask,url_for,render_template,redirect,request,flash
from flask_login import login_user,login_required,logout_user,current_user

from watchlist import app,db
from watchlist.models import User,Movie

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
    flash('该条目已删除。')
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

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        if not username or not password:
            flash('非法输入！')
            return redirect(url_for('login'))

        user=User.query.first()
        if username==user.username and user.validate_password(password):
            login_user(user)
            flash('登陆成功！')
            return redirect(url_for('index'))

        flash('无效的用户名或密码。')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('拜拜~')
    return redirect(url_for('index'))
