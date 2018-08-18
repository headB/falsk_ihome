# 注册后端编写

1. passport 一般是代表关于用户,认证,登录之类的!
2. 然后register这个处理注册的函数是这样的.
    1. ## 因为涉及到是请求注册一个新用户,所以,method是POST
    2. 请求获得参数是
        1. 手机号码(作为用户名)
        2. 短信验证码
        3. 用户输入的密码
    3. 一般视图函数的处理代码是
        ```python
        def function123():
            '''我是视图函数

            param: moblie:手机号
            param: sms_code:手机验证码
            parm: password:用户设置的密码

        ```
    4. ## request.json 只能够接受方法为POST、Body为raw，header 内容为 application/json类型的数据：对应图1
        1. https://blog.csdn.net/tengdazhang770960436/article/details/80106533
        2. body内容
            1. form-data
            2. x-www-form-urlencodeed
            3. raw
            4. binary
        3. 2.c =request.get_json()
            将请求参数做了处理，得到的是字典格式的，因此排序会打乱依据字典排序规则
            https://www.cnblogs.com/yy-cola/p/8066020.html
    5. ## 上面的步骤就成功获取到json信息并且转换到字典,然后就可以使用get去获取内容了.
    6. 检验参数,老步骤了.!
    7. 从redis拉去手机短信验证码的有关信息,看看是否存在或者是否过期了.!!
    8. ## 然后就保存信息到数据库持久化了.!
        1. 实现实例化模型类数据库
            ```python
            user = User(mobile=1324XX,password=xxxyy)
            #估计差不多这样子就可以保存数据吧
            db.session.add(user)
            db.session.commit()
            ```
        2. 更多的关于flask的数据库可以参考这里.
            通过数据库会话管理对数据库所做的改动,在 Flask-SQLAlchemy 中,会话由 db.session 表示。准备把对象写入数据库之前,先要将其添加到会话中:https://www.cnblogs.com/zknublx/p/7133750.html
        2. ## 如果出现问题.就撤销保存,db.session.rollback()
    9. 然后给数据库的手机号码字段设置为唯一字段.
    10. 然后把验证成功的验证码删除,防止用于重复验证.!
    11. ## 