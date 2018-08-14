#配置数据库
import redis
from urllib import parse
class DbConfig:
    '''配置参数'''
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"
    SQLALCHEMY_DATABASE_URI = "mysql://root:%s@localhost:3306/ihome"%parse.unquote_plus("kumanxuan@gzitcast")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    ##配置redis链接信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    #flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True #对cookie中的session_id进行隐藏.!
    PERMANENT_SESSION_LIFETIME = 86400 #session数据的有效期,单位秒



class DevelopmentConfig(DbConfig):
    '''开发环境'''
    DEBUG = True

class ProductionConfig(DbConfig):
    '''生产环境'''
    pass

config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig,
}