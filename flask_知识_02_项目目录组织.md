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

# 创建工程目录1
1. 把刚刚的DbConfig复制出来.放到新的文件
    1. 然后,上面那个作为父类,如果你需要修改什么信息的话,可以通过创建一个子类去覆盖参数.!

2. flask建议使用工厂模式.
    1. 什么是工厂模式.
        1. Python设计模式——工厂方法模式（FactoryMethod）
            https://www.cnblogs.com/Xjng/p/3879064.html
    2. 摘抄
        1. 首先我自己不是生成一个app对象吗?
            1. 如果想按<开发模式>就按这模式生成,想要<生产模式>就按这模式生成.!

3. 里面的文件夹组织很讲究的样子,前面的高度工厂化,然后后面的高度封装起来了!.
4. 关于数据库一些初始化代码放到具体那些位置会比较好一点!
    1. 整个flask项目会用到数据库和redis
    2. 你可能在models函数用到了db,也有可能在views用到了db
    3. 所以都是公共的工具,所以把db放到init文件中来.!
    4. ## 但是数据库有一个问题,创建的时候,不能第一时间绑定app,所以只能推迟去绑定.!
    5. ## 问题又来了,就是,redis究竟是放在create_app后面还是前面?
        1. 如果是公共的话,必须是放到外面.!
        2. ### 但是还有一个问题,就是,你的redis究竟是用那一个配置文件还是没有定下来的时候,
            还是,可以先创建,但是一开始为空的.!?????我大概明白了,就是先定义一个空的全局变量吧.!
            果然,里面也是这么说的.但是,为什么db并没有这样的操作.可能是因为需要绑定app参数的原因.!
5. 现在关于如何把剩下的这个视图函数也封装,一下
    1. 课件里面讲的是,在外面设置两个或者多个入口,然后,用于区分入口,例如是新版1.0,旧版2.0这样!
    2. 现在在ihome下面新建包,当作是蓝图使用,然后起名字会比较讲究一下.!
6. 会讲到RETFUL.
    1. 如何去定义路径.!
7. ## 现在,如果牵涉到数据库的话,还有迁移的问题,最好还是用相应的迁移方法.!迁移插件.!
    1. Flask Script扩展提供向Flask插入外部脚本的功能，包括运行一个开发用的服务器，一个定制的Python shell，设置数据库的脚本，cronjobs，及其他运行在web应用之外的命令行任务；使得脚本和系统分开；
8. ## 如何避免循环导包
    1. 尝试在api_1_0里面的demo文件,添加导入from ihome import db,
        这样就可以引起循环导包了.为什么??看下来讲解.
        1. 因为在demo.py文件和ihome的init文件永远在互相导入而没有去执行db这个.
    2. ### 推迟导入   解决办法就是,什么时候用就什么时候导入!
9. # 一般来说,会有两个文件夹.
    1. utils   这个文件夹代表是工具类
    2. libs 引用第三方工具包的存放位置

10. # 日志功能
    1. import logging
        1. 4种等级
            2. logging.error("String you like want to write") 是一个函数.
            3. logging.wran()
            4. logging.info()
            5. logging.debug()
    2. 设置方法
        1. logging.basecConfig(level=logging.DEBUG)
        ...............
    3. 