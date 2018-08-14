#第一步导入flask模块
from flask import Flask
import redis
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
#配置数据库
class DbConfig:
    '''配置参数'''
    SQLALCHEMY_DATABASE_URI = "mysql://root:%s@localhost:3306/ihome"%parse.unquote_plus("kumanxuan@gzitcast")
    SQLALCHEMY_TRACK_MODIFICATIONS = True



#第二步是取名
app = Flask(__name__)

app.config.from_object(DbConfig)

db = SQLAlchemy(app)

##第三步,写路由换view

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