#第一步导入flask模块
from flask import Flask

#第二步是取名
app = Flask(__name__)

##第三步,写路由换view

@app.route("/index")
def index():
    return "hello world!"

## 第四步,主函数

if __name__ == "__main__":

    app.run()