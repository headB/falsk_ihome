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
            SQLALCHEMY_DATABASE_URI = "mysql://root:kumanxuan123:3306:ihome"
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

5. ## sqlalchemy实质是独立的python操作数据库的python库.
    1. 然而在flask中,为了方便使用,被封装成为flask_sqlalchemy.
    2. ### 数据库添加密码转义,python使用urllib.parse里面的unquote_plus

6. 为flask添加redis
7. 添加csrf防护 
    1. 实质里面,用的就是装饰器.

8. 配置session,使用redis作为缓存保存数据.!
