#第一步导入flask模块
from flask import Flask
from flask_session import Session
import redis
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
import datetime
from flask_wtf import CSRFProtect
#配置数据库
class DbConfig:
    '''配置参数'''
    SQLALCHEMY_DATABASE_URI = "mysql://root:%s@localhost:3306/ihome"%parse.unquote_plus("kumanxuan@gzitcast")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    ##配置redis链接信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    ##flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True #对cookie中的session_id进行隐藏.!
    PERMANENT_SESSION_LIFETIME = 86400 #session数据的有效期,单位秒





#第二步是取名
app = Flask(__name__)

app.config.from_object(DbConfig)

db = SQLAlchemy(app)

#为flask补充csrf防护
CSRFProtect(app)

redis_store = redis.StrictRedis(host=DbConfig.REDIS_HOST,port=DbConfig.REDIS_PORT)

##第三步,写路由换view

#利用flask-session,将session数据保存到redis中
#修改配置文件,把session保存到redis中.
Session(app)


@app.route("/index")
def index():
    return "hello world!"


##创建模型类
# class User(db.Model):
#     '''测试数据库'''
#     __tablename__  = 'df_goods_info'

## 第四步,主函数

if __name__ == "__main__":
    
    app.run(debug=True)