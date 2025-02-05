import unittest

from watchlist import app,db
from watchlist.models import Movie,User
from watchlist.commands import forge,initdb

class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        #更新配置
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        #创建数据库和表
        db.create_all()
        #创建测试数据，一个用户，一个电影条目
        user=User(name='Test',username='test')
        user.set_password('123')
        movie=Movie(title='测试电影标题',year='2019')
        #使用add_all()方法一次添加多个模型类实例，传入列表
        db.session.add_all([user,movie])
        db.session.commit()

        self.client=app.test_client()   #创建测试客户端
        self.runner=app.test_cli_runner()   #创建测试命令运行器

    def tearDown(self):
        db.session.remove() #清楚数据库会话
        db.drop_all()   #删除数据库表

    #测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    #测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    #测试电影ORM类
    def test_Movie(self):
        self.assertEqual('<Movie 测试电影标题>',repr(Movie.query.get('1')))

    #测试404页面
    def test_404_page(self):
        response=self.client.get('/nothing')    #传入目标URL
        data=response.get_data(as_text=True)
        self.assertIn('页面没找到 - 404',data)
        self.assertIn('返回',data)
        self.assertEqual(response.status_code,404)  #判断相应状态码

    #测试主页
    def test_index_page(self):
        response=self.client.get('/')
        data=response.get_data(as_text=True)
        self.assertIn('Test的观影清单',data)
        self.assertIn('测试电影标题',data)
        self.assertEqual(response.status_code,200)

    #辅助方法，用于登入用户
    def login(self):
        self.client.post('/login',data=dict(
            username='test',
            password='123'
        ),follow_redirects=True)

    #测试创建条目
    def test_create_item(self):
        self.login()

        #测试创建条目操作
        response=self.client.post('/',data=dict(
            title='新电影',
            year='2019'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('已创建！',data)
        self.assertIn('新电影',data)

        #测试创建条目操作，但电影标题为空
        response=self.client.post('/',data=dict(
            title='',
            year='2019'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('已创建！',data)
        self.assertIn('非法输入！',data)

        #测试创建条目操作，但电影年份为空
        response=self.client.post('/',data=dict(
            title='新电影',
            year=''
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('已创建！',data)
        self.assertIn('非法输入！',data)

    #测试更新条目
    def test_update_item(self):
        self.login()

        #测试更新页面
        response=self.client.get('/movie/edit/1')
        data=response.get_data(as_text=True)
        self.assertIn('编辑条目',data)
        self.assertIn('测试电影标题',data)
        self.assertIn('2019',data)

        #测试更新条目操作
        response=self.client.post('/movie/edit/1',data=dict(
            title='新电影已编辑',
            year='2019'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('条目已更新。',data)
        self.assertIn('新电影已编辑',data)

        #测试更新条目操作，但电影标题为空
        response=self.client.post('/movie/edit/1',data=dict(
            title='',
            year='2019'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('条目已更新。',data)
        self.assertIn('新电影已编辑',data)

        #测试更新条目操作，但电影年份为空
        response=self.client.post('/movie/edit/1',data=dict(
            title='新电影已再次编辑',
            year=''
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('条目已更新。',data)
        self.assertNotIn('新电影已再次编辑',data)
        self.assertIn('非法输入！',data)

    #测试删除条目
    def test_delete_item(self):
        self.login()

        response=self.client.post('/movie/delete/1',follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('该条目已删除。',data)
        self.assertNotIn('测试电影标题',data)

    #测试登陆保护
    def test_login_protect(self):
        response=self.client.get('/')
        data=response.get_data(as_text=True)
        self.assertNotIn('登出',data)
        self.assertNotIn('设置',data)
        self.assertNotIn('<form method="post">',data)
        self.assertNotIn('删除',data)
        self.assertNotIn('编辑',data)

    def test_invalid_user(self):
        response=self.client.post('/',data=dict(
            username='test',
            password='456'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('登陆',data)
        self.assertNotIn('删除',data)
        self.assertNotIn('编辑',data)

    #测试登陆
    def test_login(self):
        response=self.client.post('/login',data=dict(
            username='test',
            password='123'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('登陆成功！',data)
        self.assertIn('登出',data)
        self.assertIn('设置',data)
        self.assertIn('删除',data)
        self.assertIn('编辑',data)
        # self.assertIn('<form method="post">',data)

        #测试使用错误的密码登陆
        response=self.client.post('/login',data=dict(
            username='test',
            password='456'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('登陆成功!',data)
        self.assertIn('无效的用户名或密码。',data)

        #测试使用错误的用户名登陆
        response=self.client.post('/login',data=dict(
            username='wrong',
            password='123'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('登陆成功！',data)
        self.assertIn('无效的用户名或密码。',data)

        #测试使用空用户名登录
        response=self.client.post('/login',data=dict(
            username='',
            password='123'
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('登陆成功！',data)
        self.assertIn('非法输入！',data)

        #测试使用空密码登陆
        response=self.client.post('/login',data=dict(
            username='test',
            password=''
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('登陆成功！',data)
        self.assertIn('非法输入！',data)

    #测试登出
    def test_logout(self):
        self.login()

        response=self.client.get('/logout',follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('拜拜~',data)
        self.assertNotIn('登出',data)
        self.assertNotIn('设置',data)
        self.assertNotIn('删除',data)
        self.assertNotIn('编辑',data)
        self.assertNotIn('<form method="post">',data)

    def test_settings(self):
        self.login()

        #测试设置页面
        response=self.client.get('/settings')
        data=response.get_data(as_text=True)
        self.assertIn('设置',data)
        self.assertIn('你的名字',data)

        #测试更新设置
        response=self.client.post('/settings',data=dict(
            name='meiyu',
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertIn('设置已更新。',data)
        self.assertIn('meiyu',data)

        #测试更新设置，名称为空
        response=self.client.post('/settings',data=dict(
            name='',
        ),follow_redirects=True)
        data=response.get_data(as_text=True)
        self.assertNotIn('设置已更新。',data)
        self.assertIn('非法输入！',data)

    #测试虚拟数据
    def test_forge_command(self):
        result=self.runner.invoke(forge)
        self.assertIn('数据已导入。',result.output)
        self.assertNotEqual(Movie.query.count(),0)

    #测试初始化数据库
    def test_initdb_command(self):
        result=self.runner.invoke(initdb)
        self.assertIn('数据库初始化完毕。',result.output)

    #测试删除数据库
    def test_drop_command(self):
        result=self.runner.invoke(initdb,args=['--drop'])
        self.assertEqual(Movie.query.count(),0)

    #测试生成管理员账户
    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result=self.runner.invoke(args=['admin','--username','meiyu','--password','123'])
        self.assertIn('创建用户中......',result.output)
        self.assertIn('完成。',result.output)
        self.assertEqual(User.query.count(),1)
        self.assertEqual(User.query.first().username,'meiyu')
        self.assertTrue(User.query.first().validate_password('123'))

    #测试更新管理员账户
    def test_admin_command_update(self):
        #使用args参数给出完整的命令参数列表
        result=self.runner.invoke(args=['admin','--username','peter','--password','456'])
        self.assertIn('更新用户中......',result.output)
        self.assertIn('完成。',result.output)
        self.assertEqual(User.query.count(),1)
        self.assertEqual(User.query.first().username,'peter')
        self.assertTrue(User.query.first().validate_password('456'))

if __name__ == '__main__':
    unittest.main()
