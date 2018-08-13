# 在单一文件中构建所有依赖工具

1. flask并没有官方组织方法.目录排列结构.!
2. 举例:
    ```python
        from flask import Flask
        app = Flask(__name__)
        
        @app.route("/index")
        def index():
            return "index page"
        
        if __name__ == '__main__':
            app.run()
    ```
3. 添加配置信息
    ```python
        from flask_sqlalchemy import SQLAlchemy

        class Config(object):
        '''配置信息'''
            DEBUG = True
            SECRET_KEY = "as&^*^&%(*&)(*hhuoioih)"
            #数据库
            SQLALCHEMY_DATABASE_URL = "mysql://root:kumanxuan123:3306:ihome"
            SQLALCHEMY_TRACK_MODIFICATIONS = True

        app.config.from_object(Config)

        db = SQLAlchemy(app)

        
    ```
4. 添加缓存
    ```python

        REDIS_HOST = '127.0.0.1'
        REDIS_PORT = 6379
        import redis
        #创建redis连接对象
        redis_store = redis.StrictRedis(host=localhost,port=6379,)
    ```