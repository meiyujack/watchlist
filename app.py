from flask import Flask,url_for,render_template
app=Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)

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
