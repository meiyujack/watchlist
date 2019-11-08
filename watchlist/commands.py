import click

from watchlist import app,db
from watchlist.models import User,Movie


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
