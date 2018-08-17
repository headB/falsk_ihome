# 图片验证码原理

1. 相关截图可以看8月15日的相关信息.有道云笔记.
2. ## 关于有效期
    1. 保存到内存是否可以?
        1. 可以,但是如果用户过了一年,验证码还是存在,还有没有意义?
    2. 如果保存到数据库呢?
        1. 数据库是持久保存,这样不太好.!
    3. 最好就是放到redis当中!.
        1. 将验证码的真实值存放到redis.
    4. ## 验证码要和编号一起传递
    5. ## 用户访问的时候就生成一个编号给用户.!
        1. 然后用户请求验证码的时候,携带刚刚生成的编号
        2. 然后去查询redis数据库.!
        3. ### 在redis数据库使用setex,这是一个包含时间有效期的设置.这是设置一个String类型的!.
        

# RESTFUL风格介绍
- 简书介绍的RESTFUL
    https://www.jianshu.com/p/265397f812d4
    1. REST（Representational State Transfer）
        定义了一套基于Web的数据交互方式的设计风格。
    2. RESTful
        符合REST风格的API就可以叫做RESTful API。注意，本文讲到的RESTful API设计方法将是基于HTTP和JSON实现方式，但不论HTTP还是JSON都不是REST的标准。REST只是风格，没有标准。
    3. 动词、RPC
        在微信里搜索【RESTful API 设计】，出来好多文章都是说怎么在RESTful Uri里使用动词等等，这些人除了一部分是把文章拿来抄一抄的，其他的其实搞混了REST和RPC的概念了，REST强调资源，RPC强调动作，所以REST的Uri组成为名词，RPC多为动词短语。然而它们也并不是完全不相关的两个东西，本文中的实现就会参考一部分JSON-RPC的设计思想。
    4. Web Service
        这个是一个更古老的概念，有一套它的理论，不过我更倾向于把它理解成任何基于Web提供的服务。
    5. ## 设计方法及原则：
        1. 使用HTTP方法：
            更清晰API设计的可能会使用**GETPOST PUT DELETE**四种方法分别代表“查询、添加、更新、删除”等四个动作，这在概念上是符合HTTP规范的，如Google的如下API：
        2. Uri格式：
        3. 固定返回码
        4. 固定返回结构

    6. ## 综上所述，本文所探讨的API设计是这样的：
        所有API的Uri为基于HTTP的名词性短语，用来代表一种资源。

        Uri格式如文中所述。

        使用GET POST PUT DELETE四种方法分别代表对资源的“查询、添加、更新、删除”。

        服务端接收到客户端的请求之后，统一返回200，如果客户端获取到的返回码不是200，代表链路上某一个环节出了问题。

        服务端所有的响应格式为:

        {   
            “code”: -32600, 
            “message”: “Invalid Request”, 
            “data”:{ }
        }
        他们的含义分别代表：

        code为0代表调用成功，其他会自定义的错误码；
        message表示在API调用失败的情况下详细的错误信息，这个信息可以由客户端直接呈现给用户，否则为空；
        data表示服务端返回的数据，具体格式由服务端自定义，API调用错误为空

1. 非强制性,推荐方法.博士推荐的.是风格.
2. 定义后端路径是怎么定义的.
3. api后面接的都是表示资源.(一)
4. 尽量使用4中操作(四) ----.GET(获取),POST(新建),DELETE(删除),PUT(更新)
5. 尽量保留版本(二)
    1. 代码
        ```python
            http://xx/api/1.0/info
        ```
6. 如果是get资源的话,尽量不要出现动词,然后,要是出现动词的话,最好是在灾最后的名词?get=xx(三)(五)
7. 状态码
    1. 200 OK
    2. 201 CREATE
    3. 202 ACCEPT
    4. 400 错误
    5. 401 没有权限
    6. 406 用户请求格式错误
    7. 500 服务器发生错误
8. 响应结果


# 使用captcha
1. 在python3里面出现了问题,TypeError: string argument expected, got 'bytes' 
    https://blog.csdn.net/yu599207582/article/details/59109815
    1. 解决办法:
        1. 把StringIO替换成为BytesIO

# 开发流程与接口文档编写
1. 分析需求
2. 编写代码
3. 单元测试(YES,终于可以做了.....)最后再讲!.
4. 自测 ?
5. 编写接口文档
    1. 接口的名字 提供图片验证码
        ```python
        
        ```
    2. 描述信息(描述清楚接口的功能)
    3. 传入参数
    4. 返回值
    5. 举例
    ```python
    接口: 获取图片验证码
    描述: 前端访问,可以获取到验证码图片

    url: /api/v1.0/image_codes/<image_code_id>

    参数参数:
        格式:参数是查询字符串,请求体的表单,json,xml
        名字            类型      是否必须      说明
        image_code_id   字符串      是          验证图片的编码
    返回值:
        格式:     正常:图片, 异常:json
        名字        类型        是否必传        说明
        errno       字符串         否           错误代码
        errmsg      字符串         否           错误内容

    实例:xx
    '{"errno":"4001","errmsg":"保存图片验证码失败"}'
    ```
# 单元测试
1. 为什么需要测试?
    1. 一个完整的开发过程包括这几个阶段
        1. 需求分析
        2. 设计阶段
        3. 实现阶段
        4. 测试阶段
2. 测试的分类
    1. 单元测试
    2. 集成测试
    3. 系统测试
3. 与程序开发人员最密切的就是单元测试
4. ## 关于更多的整理好的资料,请参考本文件夹里面的<flask基础知识>
5. ## 用自己的话来表达<单元测试>,就是,把测试的过程记录下来,就是单元测试.!
6. ## assert 断言
    1. 代码
        ```python
        def num_div(num1,num2):
            assert isinstance(num1, int)
            assert isinstance(num2, int)
        
        print(num1/num2)

        if __name__ == '__main__':
            num_div(100,"b")
        ```
    2. ## 平时判断是用if,现在还可以用断言,assert
    3. ## 单元测试
        1. 代码
            ```python
            import unittest
            class TestClass(unittest.TestCase):

                #该方法会首先执行,相当于做测试钱的准备工作
                def setUp(self):
                    pass
                #该方法会在测试代码执行完后执行,相当于做测试后的扫尾工作
                def tearDown(self):
                    pass
                #测试代码
                #这部分定义的方法,前缀必须是test_这样的形式.!
                def test_app_exist(self):
                    pass

            ```
        2. ### 测试案例图片,请参考有道云笔记的截图,8月16日
            1. 构造测试请求,使用requests,urllib等等.
            2. #### flask 提供客户端
                1. from login import app
                2. 创建进行web请求的客户端,
                ```python
                1. client = app.test_client()
                ```
                3. 利用client客户端,模拟发送请求
                    1. ret = client.post("/login",data={})
                    2. ret是视图返回的响应对象
                    ```python
                    resp = ret.data #data是响应体的数据
                    ```
                    3. 因为login视图返回的是json字符串
                    ```python
                    resp = json.loads(resp)
                    ```
                    4. 拿到返回值进行断言测试
                    ```python
                    self.assertIn("code",resp)
                    self.assertEqual(resp['code'],1)

                    #调用
                    if __name__ == '__main__':
                        unittest.main()
                    ```
                4. 里面的截图例子分别是用pycharm的测试和自己运行test.py模块,都有.
            3. ## 单元测试,有一个特殊用法,setup
                1. 意思:在执行测试案例之前,先执行这一步.!初始化的东西.!
            4. ## 测试模式
                1. 设置 app.config["TESTING"] = True
                2. 开启以后,可以知道具体发生错误的位置发生在那个位置.

        3. ### 这个模拟提交请求,然后把返回结果对比之后,进行判断.!
            1. 但是,有意义吗?
            2. #### 需要去了解自动测试的东东.!
            3. 自動軟體測試、TDD 與 BDD
                1. https://medium.com/@yurenju/%E8%87%AA%E5%8B%95%E8%BB%9F%E9%AB%94%E6%B8%AC%E8%A9%A6-tdd-%E8%88%87-bdd-464519672ac5
                2. https://www.zhihu.com/question/49530527
                3. 


# 编写前端去用接口!
1. 生成一个边好
    1. 时间戳
    2. uuid(全局唯一标识符)

# 数据库测试
1. 首先打开app的测试,
    ```python
    app.testing = True
    ```
2. 然后导入指定的model类.
    1. 例子,from author_book import Author,db,app
3. ## setUp上面的这些操作,会在特殊函数,setUp函数里面提前加入参数,
    1. ## 测试ING.还有具体说明一下,就是前面加入的参数,包括了加入了数据库的地址,到时候测试的时候,也不会用到什么真的数据!.
4. ##tearDown 结尾.!
