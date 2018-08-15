# 提供静态文件的蓝图编写

1. ## 为static做准备!.
    1. 专门写一个视图函数去处理这个satic路径的问题.!
    2. 在ihmoe下面新建一个蓝图,单一文件,专门用于处理url处理.web_html
        1. 在web_html.py在里面url匹配地址,就好像django里面的urls的处理.!
            ```python
            from flask import Blueprint,current_app

            #提供静态文件的蓝图
            html = Blueprint("web.html",__name__)
            @html.route("/<re(r'.*'):html_file_name>")
            def get_html(html_file_name):
                '''提供html文件'''
                #如果html_file_name为空的话,表示访问的路径是/,请求的是主页
                if not html_file_name:
                    html_file_name = "index.html" 
                if html_file_name != 'favicon.ico':
                    html_file_name = "html/" + html_file_name
                return current_app.send_static_file(html_file_name)
            ```

    3. 然后在utils文件里面新建一个commons.py.
        1. 在里面定义正则转换器,继承一个基本的,然后返回一个自定义的!.
        ```python
        # coding:utf-8
        from werkzeug.routing import BaseConverter
        # 定义正则转换器
        class ReConverter(BaseConverter):
            """"""
            def __init__(self, url_map, regex):
                # 调用父类的初始化方法
                super(ReConverter, self).__init__(url_map)
                # 保存正则表达式
                self.regex = regex
        ```
    4. 然后在ihome的init文件里面导入.
        ```python
        #为flask添加自定义的转换器
        app.url_map.converters['re'] = ReConverter
        #注册提供静态文件的蓝图
        from ihome import web_html
        app.register_blueprint(web_html.html)
        return app
        ```
    5. 在这里,勉强看得懂,就是,这里利用了吧把html的名字转换了一下.匹配正则!.
    ```python
    @html.route("/<re(r'.*'):html_file_name>")
    ```

# csrf防护机制
1. 从cookie中获取一个大概叫csrf_token的值,
2. 从请求体中获取一个csrf_token的值
3. 如果两个值相同,则检验通过,可以进入到视图函数中执行,
    如果两个值不同,则检验失败,会向前端返回状态码400的错误!
4. 跨站攻击.!
5. 有一个插图,可以参考一下有道云笔记,2018年8月15日. 
6. csrf跨站攻击.
    1. Web安全之CSRF攻击的防御措施
        https://www.cnblogs.com/cxying93/p/6035031.html
7. ## 防御办法
    1. 尽量使用POST，限制GET
    2. 浏览器Cookie策略
    3. 加验证码
    4. Referer Check
    5. Anti CSRF Token
        现在业界对CSRF的防御，一致的做法是使用一个Token（Anti CSRF Token）。
        例子：
        1. 用户访问某个表单页面。
        2. 服务端生成一个Token，放在用户的Session中，或者浏览器的Cookie中。
        3. 在页面表单附带上Token参数。
        4. 用户提交请求后， 服务端验证表单中的Token是否与用户Session（或Cookies）中的Token一致，一致为合法请求，不是则非法请求。
        这个Token的值必须是随机的，不可预测的。由于Token的存在，攻击者无法再构造一个带有合法Token的请求实施CSRF攻击。另外使用Token时应注意Token的保密性，尽量把敏感操作由GET改为POST，以form或AJAX形式提交，避免Token泄露。
        注意：
        CSRF的Token仅仅用于对抗CSRF攻击。当网站同时存在XSS漏洞时候，那这个方案也是空谈。所以XSS带来的问题，应该使用XSS的防御方案予以解决。
8. 什么是xss攻击.
    1. 跨站脚本功攻击，xss，一个简单的例子让你知道什么是xss攻击
        https://blog.csdn.net/Ideality_hunter/article/details/80621138

9. ## 同源策略

    1. 限制了不同源的网站不能相互操作资源.


# 如何设置csrf防护
1. 看情况
    1. 前后端不分离,直接在模板植入csrf_token()就可以了!

# send_static_file
