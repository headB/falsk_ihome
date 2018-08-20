# 登陆后逻辑编写

1. ## 登录状态需要保存到session当中
2. 这个逻辑还是写在passport当中.
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

# 前端
1. 测试的时候用的是postman,仅仅用于测试的.!
    1. ## 可以在body里面raw写json格式的数据.
2. 前端的日常登录