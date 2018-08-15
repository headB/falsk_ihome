# 提供静态文件的蓝图编写
1. 为static做准备!.
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
        ```pyhton
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