from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect #引入csrf包
from flask_cache import Cache #引入缓存

import pymysql
pymysql.install_as_MySQLdb()

#惰性加载
csrf = CSRFProtect()
models = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE':'simple'})

def create_app(config_name):  #创建app示例的方法
    #创建app实例
    app = Flask(__name__)
    app.config.from_object('settings.DebugConfig')  #引入settings.py文件下的内容
    # app.run(threaded = True) #小规模调优
    #app惰性加载插件
    csrf.init_app(app)    #惰性加载
    models.init_app(app)
    cache.init_app(app)

    #注册蓝图
    from .main import main as main_blueprint
    from app.ApiResource import api_main
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_main,url_prefix = '/api') #路由拼接的前部分

    return app

