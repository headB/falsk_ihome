# 云通讯介绍
1. 先注册
2. 然后稍微看一下模板.
3. 然后去SDK下载一个东东!demo.测试压缩包
    https://www.yuntongxun.com/doc/ready/demo/1_4_1_2.html
4. 然后,我们想发短信的时候,调用一下函数就可以了.
    1. 但是,好像有个但是,看看什么情况.!
    2. 但是在调用send_template,已经持续在跟云通讯通信了.
    3. 先拿到凭据,然后再进行通信.
    4. ## 然后每次都调用上面的代码,重复去调用,会有延迟,所以可以自定义一个类.!
5. 然后把一些不应该重复的代码,就封装在类里面,但是又必须第一时间运行,就放到__init__里面就可以了.
    1. 但是,注意了,如果这些代码需要被调用的话,还得设置赋值给self,不然的话,不好共享啊~.不设置就变成局部变量了.!
6. 然后还可以设置一个单例模式.
    1. 忘记返回的是调用父类的new方法.
    2. 除非是第一次实例化,返回父类的new方法,否则,都是返回已经实例化过的单类.
        1. 这个例子里面,学到了,就是如果都是返回同一个类型的数值,判断条件又只有两个,就可以这样了,挺灵活的.!
        ```python
        def __new__(cls):
        if cls.tag !=None:
            return super().__new__(cls)
        return cls.tag
        ```
    3. ## 对,如果该文件不是被调用,如果这个文件,作为单独运行的,或者入口的话,都得设置 if __name__ = "__main__"来运行,
    这是一个好习惯.!
    4. 这...传智介绍的短信.....太烂了....都是基于python2的....意思是,我得精通python3..太好了.当做练习.!
7. python3里面,不建议使用urllib了.
8. python3里面,字典取消了iteritems(),直接被items()取缔了.!

# 路由url地址转化原来就叫过滤器.

1. 这是是关于简书的一遍文章,说的就是转换器.
    https://www.jianshu.com/p/ce3028e9546e
2. ## 在flask中使用jsonify和json.dumps的区别
    https://blog.csdn.net/Duke_Huan_of_Qi/article/details/76064225
    1. 所以说,在flask中的话,就尽量多用jsonify.
3. ## 获取get过来的参数
    1. 写法是 xx = request.args.get("xxx")
    2. 然后使用if not all(['xx','yy'])
    3. 然后我观察了一下路由和函数的关系
    ```python
    @api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
    def get_sms_code(mobile):
    ```
    > 恩恩,顾名思义
4. ## 看一下flask操作数据库先!
    1. ### 从redis获取str类型数据
    ```python
        redis_store.get('xxx')
    ```
    2. ### 如果发生错误,调用当前的 currect_app.logger.error(e)
    3. 记得经常返回json数据的话,用 return jsonify
    4. ### 获取模型类的数据
    ```python
    from models import xxx
    User.query.filter_by(mobile=mobile).first()
    ```
    5. 如果查询手机号码异常的话,就继续往下走.暂时不管了.!
    6. 生成手机验证码>!
        1. 生成随机数.使用random,---> sms_code = "%06d" % random.randint(0, 999999)
        2. ### 字符串格式符."%06",注意了,6前面的0,意思是,这是一个固定的6位数,如果这个整数不足6位数的话,就自动补充0.
        3. ### 保存真实验证码内容
            1. 也是使用setex
