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

# 前端修改

1. 修改表单
    1. method用post请求方式
2. ## 需要拦截表单,因为一些校验步骤需要验证正确之后才可以提交
    1. ### 为什么这样做?因为表单提交的数据格式不是真正的json格式,需要用ajax格式化一下,用js格式化一下
    2. ### 拦截表单的方法1就是,绑定表单提交按钮,$("..formxx").submit(function(e){xxx})
    3. ### 上面的e还有故事,这个代表的是这个行为的描述信息.!
    4. ### 拦截语句是e.preventDefault()
    5. ### 关于js拦截的部分知识点
        1. preventDefault
            https://www.cnblogs.com/AndrewXu/p/4631521.html
        2. 关于js中return false、event.preventDefault()和event.stopPropagation()
            https://www.cnblogs.com/momo798/p/6025777.html
    6. ### 调用JSON.stringify(xx)将字典转换成为json数据.
    7. ### 还可以自己定义ajax来写请求,因为需要加入不少的参数,例如需要header加入'Content-Type'='application/json'
            `$.ajax({url:"/jquery/test1.txt",async:false});`
            关于手动使用ajax的一些参数说明
            http://www.w3school.com.cn/jquery/ajax_ajax.asp
            例子
            ```python
            $.ajax({
            url: "/api/v1.0/users",
            type: "post",
            data: req_json,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            }, // 请求头，将csrf_token值放到请求中，方便后端csrf进行验证
            success: function (resp) {
                if (resp.errno == "0") {
                    // 注册成功，跳转到主页
                    location.href = "/index.html";
                } else {
                    alert(resp.errmsg);
                }
            }
            ```
    8. ### 跨站调用的问题,在当前某一个网站直接使用ajax调用其他网站的话,这是一个不怎么允许的操作.!
    9. ### 原来jquery并不能直接调用cookie的.

# 密码加密与property装饰器使用
1. md5已经变成不安全了.!
    1. 暴力破解,已经有大量的对比密码资料了.!
    2. 数学方法反推!
2. ## 建议使用sha256
3. ## 在models那边进行密码加密,不在视图那边加密密码了.!
    1. ### 使用werkzeug的security的generate_password_hash
    2. ### 在flask里面已经提供了一个函数,用于加密和解密的校验!.
    3. generate_password_hash的介绍
        1. method就是加密的方式
            1. pbkdf2:sha256
            2. salt_lenth 盐值长度
            3. 然后返回盐值和计算结果.!
            4. #### 盐值和密码要放在一起.!
        2. ### 我观察到的就是,这个加密的步骤写在了models那边去了,然后在外面调用数据库模型类的时候挺方便的.
            1. 先调用加密的函数.
            2. 然后将获取到的值再保存到数据库当中就可以了.!
4. ## 知识点应用,装饰器,@property把函数封装一下,变成属性,可以用于设置值.
    1.  代码
    ```python
    class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
    ```
5. ## 方法有三种:
    1. 对象方法
    2. 类方法
    3. 静态方法
6. 上面说到的,使用装饰器的问题,现在思考一下,就是,
    1. 使用property的话,一个涉及到读取问题,一个涉及到设置值的问题
    2. 如果是涉及到设置数值的话,就需要检查变量,然后再设置数值
    3. ### 如果都是设置好装饰器这种模式的话,设置保存密码就很方便了.!