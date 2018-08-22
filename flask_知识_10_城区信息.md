# 发布新房源
1. ## 城区信息
    1. ### 因为这个信息经常被调用,所以,要充分利用好redis+mysql配合使用.
    2. flask的日常查询数据库`area_li = Area.query.all()
    3. try ...Exception可以配合使用else
        1. 意思是,代码
        ```python
        try:
            function(xxx)
        except Exception as e:
            return xx
        else:
            #意思就是,假如没有错误的话,就运行这里
        ```
    4. `to python`和`to dict`
        1. 将对象转换为字典.
        ```python
        def to_dict():
            d = {
                "a":'xx',
            }
        ```
        2. 然后其他函数就可以调用这个转换函数了
        3. ### 上面的转换是在models里面设置的.!

# 缓存机制
1. 首页大量去访问,所以得有缓存机制.
2. 首先去redis里面获取数据
    1. 如果没有数据,就去mysql去获取数据
    2. 然后顺便保存一份数据到redis
    3. 下一次获取数据的时候,重复上面的步骤.
    4. 这样子,多数重复的数据就可以去redis获取了.!
3. ## 问题,数据不同步
    1. 一定要设置有效期,
    2. ### 解决方法
        1. 在操作mysql的时候,删除缓存数据
        2. 给redis缓存数据设置有效期,保证过了有效期,缓存数据会被删除

# 用户模块修改
1. ## 在关于RESTFUL定义里面,修改信息,应该用`PUT`方法
2. 所以修改用户,提交的方法就使用put方法.
3. ## 因为在曾经写了一个装饰器,里面验证用户身份之后,会自动将用户的id自动保存到全局变量g对象中.
    1. 然后在传过来的json格式的信息进行分类.
    2. g对象的定义
        `名字:g：global` 
        1. g对象是专门用来保存用户的数据的。 
        2. g对象在一次请求中的所有的代码的地方，都是可以使用的。(感觉像超全局对象)
4. ## 为了保证名字的唯一性,所以,就需要去查询数据库.
5. ## 然后日常操作数据库,都是使用commit,rollback,之类的.!
6. ## 还有一个就是如果成功修改了用户之后,记得session里面的名字也要记得一起修改.
7. 在返回头像的时候,
    1. 如果用户存在头像的url地址的话,就给拼接前面的域名,不然的话,就返回为空就可以了.
8. 调用当前对象的`create_time.strftime("%Y-%m-%d %H:%M:%S")`,可以方便保存时间在数据库里面.!
    1. 上面的create方法,原来取之于上面的基类里面的create_time来的,然后上面的用于是把当前时间转换格式.方便调用.!

# 实名认证
1. 定义视图
2. 用route和login_required去装饰这个函数.
3. 反正就是一个普通的查询
4. ## 另外一个接口就是专用用于设置用户的认证信息
    1. 请求方式是POST,第一次访问就使用POST.
    2. ### 用户只能设置一次实名设置信息
        1. 进行判断,加入user里面的id_card和real_name都为空才进行设置信息
        flask日常数据库查询
        `User.query.filter_by(id="xx",real_name=None,id_card=None)
5. 日常前端
    1. 用ajax提交信息,很多时候都得传递json格式的数据,所以得用stringify,将字典类型转换为json格式!
    2. 想想,如果用$.post的话,后面的传递不是也是字典吗?
        1. 看了一下资料,关于$.post的参数说明,就是,最后一个dataType,原来是大概说让服务器可以返回哪些信息.
    3. 然后都是叭叭叭日常前端信息判断和跳转.

# 城区信息前端编写与前端模板的使用
1. 后端已经写好了,现在看看前端要怎么编写.
2. 前端接收后端传递过来的城区信息进行展示.
    1. ## 老生常谈了,也是在定义加载好了之后,写js函数.
        1. 关于在js的遍历
            1. for循环
            ```js
            for (i=0;i>=x;i++){xx}
            ```
        2. 然后对内容进行追加.对目标对象,进行下标迭代遍历.
        ```js
        for (i=0; i<areas.length; i++) {
                var area = areas[i];
                $("#area-id").append('<option value="'+ area.aid +'">'+ area.aname +'</option>');
            }
        ```
3. ## 使用js模板,上面的操作的确可以通过后台获取到信息并且在前台展示,但是,现在有更加简便的方法.
    1. ### 使用ART-TEMPLATE--高性能javascript 模板引擎 腾讯前员工开源的https://aui.github.io/art-template/zh-cn/docs/index.html
        1. 实现.
        2. 引入,在jq后面引入`xx/js/template.js`
    2. ### 定义模板
        1. 找位置定义模板
        ```js
        <script type="text/html" id="编号名字" > 
        {{each areas as area }}
        <option value="{{area.aid}}">{{ area.aname }}</option>
        {{/each}}
        </script>
        ```
        2. 然后ajax获取到数据之后,把这些数据放塞到模板里面.
        3. 然后再利用js去渲染
    3. ### 自己感觉就是少了去操作选择器了,不过也挺好的,对于熟悉选择器的人来说!
    4. ### 使用template函数
        1. 代码,注意了,下面里面的id-xx就是关键了,对象上面说的id="编号名字"了.
        ```js
        var html_text = template("id-xx",{areas:areas})
        $("area-id").html(html);
        ```
        2. 这些东西看起来很jijia2X
        3. 有个截图,可以看有道云的笔记.2018年8月22日



# 关于谷歌,关于如何查看网站加载模式,关于chrome,利用开发者工具,就是F12,然后找到source,就可以查看具体的运行过程了.