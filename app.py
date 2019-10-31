from flask import Flask,url_for
app=Flask(__name__)


@app.route('/')
@app.route('/index')
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
