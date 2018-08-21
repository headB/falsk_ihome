# 登陆后逻辑编写

1. ## 登录状态需要保存到session当中
2. 这个逻辑还是写在passport当中.
    1. 设置一个路由路径先.
3. 老生常谈了.
    1. 接收参数
    2. 校验参数
        1. 看看参数是否完整
    3. 业务逻辑
4. ## 登录
    1. 注意了,这个是登录,不是注册
        1. 所以,首先得防止一下非法的暴力破解
        2. 根据手机号码查询数据库
        3. 对比账号密码
            1. 如果验证成功,就保存登录状态,
            2. 如果验证失败,记录错误次数,返回信息
5. ## 具体的代码实现
    1. 获取数据 `request.get_json()` #估计会自己转换成为字典,方便调用
    2. ### flask获取用户的远程IP地址 `request.remote_addr`
        1. #### 拓展 django的远程获取用户IP地址 `request.META['REMOTE_ADDR']`
        2. 记得经常用异常去排除错误!
        3. 还有配置日志错误记录
    3. flask日常数据库查询 `User.query.filter_by(mobile=mobile).first()`
    4. flask日常返回json数据 `return jsonify(xx)
    5. ### 又涉及到密码的问题了,所以这次的代码,验证密码的这一部分,得在models里面定义好函数和进行!
    ```python
    def check_passwd(self,passwd):
        '''
        :param passwd: 用户登录时候提交的原始密码
        :return : 如果正确
        '''
        return check_password_hash(self.password_hash,passwd)
    ```
    6. 如果登录失败了,也记得记录喔.!
    7. ### redis有一个函数专用用来做加减的.
        1. INCR
            1. Redis Incr 命令将 key 中储存的数字值增一。
                如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作。
                如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
                本操作的值限制在 64 位(bit)有符号数字表示之内。
        2. 然后,这个登录错误的信息也是设置一个限度.
    8. 登录成功,保存到session会话当中!.

# 关于测试,的确是的,用一个外部的,可以随意get,post的软件,操作,测试,的确是想当方便的.!

# 前端
1. 测试的时候用的是postman,仅仅用于测试的.!
    1. ## 可以在body里面raw写json格式的数据.
2. 前端的日常登录
    1. 利用postman进行日常的测试!
    2. 

# 使用postman测试前端登陆
1. ## 具体的测试结果,请查看云笔记的,2018年8月21号的笔记详情.!
2. ## 记住了,json的严格格式是都是使用双引号的,""
3. ## 测试了,密码错误之后,就阻止登陆了!

# 检查登陆状态与退出代码
1. ## 原来这个讲师都准备讲了,只是我以为他在之前已经设置了登陆检查,晕,以后还是跟着视频来吧.!
2. ## 由于登陆,属于查询,所以,是GET查询了.! `@api.route("/session",methods=['GET'])`
    1. 在session中尝试获取当前的session值. `name = session.get("name")`
        1. 如果能获取得到值的话,就是登陆过了,并且返回name值
3. ## 如果是退出的话,由于是属于删除session的值,所以方式是DELETE `@api.route("/session",methods=["DELETE"])`
    1. ### 清除当前用户的session值.`session.clear()`
4. 然后就是查看一下前端的代码
    1. ## 某种原因,前端页面的登陆和注册按钮,还有用户地址栏,显示属性都是`display:none`,应该是css设置的.继续.
5. ## 还得继续说说退出这个地方,`logout`,但是需要用delete方法,所以得用ajax方式去退出了.!
    1. ### 我设置头部请求的时候,ajax设置的时候也是设置`headers`的.!注意了.

# 登陆验证装饰器
1. 个人信息
    1. 闭包的应用.
2. ## 关于用户认证,用户登陆的问题,想想以前的django,才用的是定义一个自定义的,继承于Login_view的模块.
    1. ### 然后是添加到urls,因为所有的请求都必须在这里分流,所以在这里添加认证.
    2. ### 但是项目里面的话,是在具体那个view需要权限的时候才继承这个自定义认证类.
3. ## 用户认证,flask这里的做法,发酸是在commons.py写一个验证装饰器
    1. 然后装饰器里面调用了一次去获取session_id的数值
        1. ### 然后里面的视图函数也想向刚刚的装饰器获取他们的数值.
            1. 这个时候得借助中间人了,引入中间人,g对象,`from flask import g`,是一个全局变量!.估计是基于session的吧.
    2. ### 在装饰器的内层函数当再加装装饰器 
        1. 先导入`import functools`
        2. `functools.warpper`专门用来装饰内层函数
        3. 什么是说明文档
            1. 就是类或者函数里面的一对'''或者"""里面的内容,就是说明文档了.
            ```python
            def test():
                """
                其实我就是说明文档了.!
                """
            ```
        4. ### 使用装饰器,不应该去改变被装饰的函数,一般默认的装饰方法会修改的
        ```python

        def test_wrapper(func):

            def test_func(*args,**kwargs):
                pass
            return test_func

        def test():
            """good"""
            pass
        
        print(test.__name__)#这里的值不再等于test了
        print(test.__doc__)#这里也不存在数值了.

        ```
        5.  应对上面的办法就是,使用functools去返回被装饰函数的属性,
        ```python
        @functools.wraps(func)
        def wrapper(*args,**kwargs)
        ```
    3. 