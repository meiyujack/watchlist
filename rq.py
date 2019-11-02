from flask import Flask,render_template
from flask import request

app=Flask(__name__)
app.debug=True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rq/')
def get_request():
    path=request.path
    method=request.method
    name=request.args.get('name')
    if name:
        return name
    else:
        return '没找到'

if __name__ == '__main__':
    app.run()
