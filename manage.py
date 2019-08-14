from app import create_app,models  #导入app就会导入执行app下init文件中的方法
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from gevent import monkey #猴子补丁，将之前代码中所有不切合协程的代码改为切合的
monkey.patch_all() #给所有打补丁

#实例化app
app = create_app('running')   #app下init文件中有create_app方法，所有在这里可以调用

manager = Manager(app)        #命令行封装app

migrate = Migrate(app,models) #绑定可以管理的数据库模型

manager.add_command('db',MigrateCommand)  #加载数据库管理命令，命令格式为：python manage.py db 命令

#协程调优
@manager.command
def runserver_gevent():
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('127.0.0.1',5000),app) #调用127.0.0.1和5000,
    server.serve_forever() #使用forever()运行


if __name__ == '__main__':
    manager.run()       #从manage.py下可以运行shell命令