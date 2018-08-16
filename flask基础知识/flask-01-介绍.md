# 1.1 了解Flask：

***Web应用程序的本质：***
 Web(World Wide Web)诞生最初的目的，是为了利用互联网交流工作文档。

 ![HTTP请求过程](/images/http_request.png)

- 一切从客户端发起请求开始。
  - 所有Flask程序都必须创建一个程序实例。
  - 当客户端想要获取资源时，一般会通过浏览器发起HTTP请求。
  - 此时，Web服务器使用一种名为WEB服务器网关接口的WSGI（Web Server Gateway Interface）协议，把来自客户端的请求都交给Flask程序实例。
  - Flask使用Werkzeug来做路由分发（URL请求和视图函数之间的对应关系）。根据每个URL请求，找到具体的视图函数。
  - 在Flask程序中，路由一般是通过程序实例的装饰器实现。通过调用视图函数，获取到数据后，把数据传入HTML模板文件中，模板引擎负责渲染HTTP响应数据，然后由Flask返回响应数据给浏览器，最后浏览器显示返回的结果。

### 为什么要用Web框架？

 web网站发展至今，特别是服务器端，涉及到的知识、内容，非常广泛。这对程序员的要求会越来越高。如果采用成熟，稳健的框架，那么一些基础的工作，比如，安全性，数据流控制等都可以让框架来处理，那么程序开发人员可以把精力放在具体的业务逻辑上面

1. 稳定性和可扩展性强

- ，可以降低开发难度，提高开发效率。

 总结一句话：{% em color="#fff700" %}避免重复造轮子。{% endem %}



### Flask框架的诞生：

 Flask诞生于2010年，是Armin ronacher（人名）用Python语言基于Werkzeug工具箱编写的轻量级Web开发框架。它主要面向需求简单的小应用。

 Flask本身相当于一个内核，其他几乎所有的功能都要用到扩展（邮件扩展Flask-Mail，用户认证Flask-Login），都需要用第三方的扩展来实现。比如可以用Flask-extension加入ORM、窗体验证工具，文件上传、身份验证等。Flask没有默认使用的数据库，你可以选择MySQL，也可以用NoSQL。其 WSGI 工具箱采用 Werkzeug（路由模块） ，模板引擎则使用 Jinja2 。

 可以说Flask框架的核心就是Werkzeug和Jinja2。

 Python最出名的框架要数Django，此外还有Flask、Tornado等框架。虽然Flask不是最出名的框架，但是Flask应该算是最灵活的框架之一，这也是Flask受到广大开发者喜爱的原因。


 **Flask扩展包：**
 + Flask-SQLalchemy：操作数据库；
 + Flask-migrate：管理迁移数据库；
 + Flask-Mail:邮件；
 + Flask-WTF：表单；
 + Flask-Bable：提供国际化和本地化支持，翻译；
 + Flask-script：插入脚本；
 + Flask-Login：认证用户状态；
 + Flask-OpenID：认证；
 + Flask-RESTful：开发REST API的工具；
 + Flask-Bootstrap：集成前端Twitter Bootstrap框架；
 + Flask-Moment：本地化日期和时间；



 1. 中文文档（[http://docs.jinkan.org/docs/flask/](http://docs.jinkan.org/docs/flask/)）
 2. 英文文档（[http://flask.pocoo.org/docs/0.11/](http://flask.pocoo.org/docs/0.11/)）


# 1.2 Flask和django对比
### 框架之间的差别
 Django的一站式解决的思路能让开发者不用在开发之前就在选择应用的基础设施上花费大量时间。Django有模板，表单，路由，认证，基本的数据库管理等等内建功能。与之相反，flask包含路由和验证，但是模板和数据库管理需要第三方库。

用Flask来构建应用之前，选择组件的时候会给开发者带来更多的灵活性 ，可能有的应用场景不适合使用一个标准的ORM，或者需要与不同的工作流和模板系统交互。

Flask创始于2010年年中。Django发布于2006年,是非常成熟的框架，积累了大量的插件和扩展来满足不同需要。

尽管Flask的历史较短，但它能够从以前的框架学到一些东西并且将它的目标设定在了小型项目上。它在一些仅有一两个功能的小型项目上得到了大量应用。比如httpbin这样的项目，简单但非常强大，是一个帮助debug和测试HTTP的库。


### 社区

 Django的社区是最活跃的，在StackOverflow上有80000个相关问题和大量的博客和强大的用户。Flask的社区就没有这么大了，但是它们的社区在邮件列表和IRC里还是挺活跃的。在StackOverflow上只有5000个相关问题，Flask比Django的关注度小15倍。在Github上，它们的stars数相近。

### 入门引导
Flask的Hello World应用的代码是最简单的，只用在一个Python文件里码7行代码就够了。 
	from flask import Flask 
	app = Flask(__name__) 
	
	@app.route("/")
	def hello(): 
	    return "Hello World!" 
	
	if __name__ == "__main__":
	    app.run()
这就是为什么Flask没有引导工具：因为它根本不需要。从上面的Hello World应用的特点来看，一个没什么Python web开发经验的人就可以很快的上手开始撸代码。

对于需要把组件分离开的项目，Flask有blueprints。例如，你可以这样构建你的应用，将与用户有关的功能放在user.py里，把与销售相关的功能放在ecommerce.py里。
Django拥有自己的引导工具,它是django-admin的一部分
	django-admin startproject hello_django 
	django-admin startapp hello
我们已经可以看到Django和flask的一些区别。Django把一个项目分成各自独立的应用，而Flask认为一个项目应该是一个包含一些视图和模型的单个应用。也可以在Flask里复制出像Django那样的项目结构，但那不是默认的。
![django框架结构](/images/project_structure.png)
默认情况下，Django只包含空的模型和模板文件，一个新的用户可以看一点例子代码就开始工作。它也能让开发者选择如何分配Django的应用。
###模版
Django的模版大家都很熟悉,我们举一个简单的例子

```python
	<!-- view.html -->
	<div class="top-bar row">
	  <div class="col-md-10">
	  <!-- more top bar things go here -->
	  </div>
	  {% if user %}
	  <div class="col-md-2 whoami">
	    You are logged in as {{ user.fullname }}
	  </div>
	  {% endif %}
	</div>
	{% for widget in inventory %}
	   <li>{{ widget.displayname }}</li>
	{% endfor %}
```



对于大多数普通的模板任务来说，Django能够轻松实现，非常容易上手。
Flask默认使用一个受Django启发而发展起来的名为Jinja2的模板，但也可以通过配置来使用其他的语言。一个码农可能会将Django和Jinja模板弄混。事实上，所有上面的Django模板的例子在Jinja2里也是好使的。我们就不重复上面的例子了，我们来看看Jinja2比Django模板的一些更有表现力的特点。
```python
	<!-- Django -->
	<div class="categories">Categories: {{ post.categories|join:", " }}</div>
	
​```python
<!-- Jinja -->
<div class="categories">Categories: {{ post.categories|join(", ") }}</div>
```
在Jinja的模板语言里，可以把任何数量的参数传给过滤器，因为Jinja像调用一个Python函数的方式来看待它，用圆括号来封装参数。Django使用冒号来分隔过滤器名和参数，这样就只能传递一个参数了。

Jinja和Django的 for 循环很相似。我们来看看它们的区别。在Jinja2, for-else-endfor 结构让你能对一个列表进行迭代，也能处理列表为空的情况。
```python
        {% for item in inventory %}
        <div class="display-item">{{ item.render() }}</div>
        {% else %}
        <div class="display-warn">
        <h3>No items found</h3>
        <p>Try another search, maybe?</p>
        </div>
        {% endfor %}
```
在Django版本的功能是一样的，只是使用了 for-empty-endfor 这样的结构替换了 for-else-endfor 的结构。
```python
	{% for item in inventory %}
	<div class="display-item">{{ item.render }}</div>
	{% empty %}
	<div class="display-warn">
	<h3>No items found</h3>
	<p>Try another search, maybe?</p>
	</div>
	{% endfor %}
```
除了上述的语法区别,flask还提供了很多特有的上下文变量
```python
(url_for,get_flashed_messages()等)
```

#安装环境

 使用虚拟环境安装Flask，可以避免包的混乱和版本的冲突，虚拟环境是Python解释器的副本，在虚拟环境中你可以安装扩展包，为每个程序单独创建的虚拟环境，可以保证程序只能访问虚拟环境中的包。而不会影响系统中安装的全局Python解释器，从而保证全局解释器的整洁。

 虚拟环境使用virtualenv创建，可以查看系统是否安装了virtualenv：
 ```bash
$ virtualenv --version
 ```

 **安装虚拟环境**

```bash
$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper
```


**创建虚拟环境(须在联网状态下)**

```bash
$ mkvirtualenv Flask_py
```

**进入虚拟环境**

```bash
$ workon Flask_py
```

** 退出虚拟环境**

如果所在环境为真实环境，会提示deactivate：未找到命令 


```bash
$ deactivate Flask_py
```


# 1.2.1 安装Flask

```bash
指定Flask版本安装
$ pip install flask==0.10.1
pip freeze > requirements.txt
```
Mac系统：
```bash
$ easy_install flask==0.10.1
```


**在ipython中测试安装是否成功**

```bash
$ from flask import Flask
```

![安装成功1](/images/install_success1.png)

![安装成功2](/images/install_success2.png)



# 1.3 从 Hello World 开始
###Flask程序运行过程：
 所有Flask程序必须有一个程序实例。

 Flask调用视图函数后，会将视图函数的返回值作为响应的内容，返回给客户端。一般情况下，响应内容主要是字符串和状态码。

 当客户端想要获取资源时，一般会通过浏览器发起HTTP请求。此时，Web服务器使用WSGI（Web Server Gateway Interface）协议，把来自客户端的所有请求都交给Flask程序实例，程序实例使用Werkzeug来做路由分发（URL请求和视图函数之间的对应关系）。根据每个URL请求，找到具体的视图函数。
 在Flask程序中，路由的实现一般是通过程序实例的装饰器实现。通过调用视图函数，获取到数据后，把数据传入HTML模板文件中，模板引擎负责渲染HTTP响应数据，然后由Flask返回响应数据给浏览器，最后浏览器处理返回的结果显示给客户端。

## 示例：

新建文件hello.py:


导入Flask类

```
from flask import Flask
```

Flask函数接收一个参数__name__，它会指向程序所在的模块

```
app = Flask(__name__)
```

 装饰器的作用是将路由映射到视图函数index

	@app.route('/')
	def index():
	    return 'Hello World'



 Flask应用程序实例的run方法启动WEB服务器

	if __name__ == '__main__':
	    app.run()


![装饰器路由](/images/app_route.png)


### 给路由传参示例：

有时我们需要将同一类URL映射到同一个视图函数处理，比如：使用同一个视图函数 来显示不同用户的个人信息。


路由传递的参数默认当做string处理，这里指定int，尖括号中的内容是动态的
	@app.route('/user/<int:id>')
	def hello_itcast(id):
	    return 'hello itcast %d' %id

![给路由传参](/images/dynamic_route.png)


### 返回状态码示例：

	python
	@app.route('/')
	def hello_itcast():
	    return 'hello itcast',404

![404](/images/404.png)


### 重定向redirect示例

	from flask import redirect
	@app.route('/')
	def hello_itcast():
	    return redirect('http://www.itcast.cn')

![302](/images/302.png)



### 正则URL示例：


	from flask import Flask,render_template,request
	from werkzeug.routing import BaseConverter
	
	class Regex_url(BaseConverter):
		def __init__(self,url_map,*args):
			super(Regex_url,self).__init__(url_map)
			self.regex = args[0]
	
	app = Flask(__name__)
	app.url_map.converters['re'] = Regex_url
	
	@app.route('/user/<re("[a-z]{3}"):id>')
	def hello_itcast(id):
	    return 'hello %s' %id


###返回json

	python
	from flask import Flask,json
	@app.route('/json')
	def do_json():
	    hello = {"name":"stranger", "say":"hello"}
	    return json.dumps(hello)
# 1.5 上下文和扩展
### 请求上下文(request context)
Flask从客户端收到请求时,要让视图函数能访问一些对象,这样才能处理请求,请求对象是一个很好的例子,它封装了客户端发送的HTTP请求.
要想让视图函数能够访问请求对象,一个显而易见的方式是将其作为参数传入视图函数,不过这会导致程序中的每个视图函数都增加一个参数,除了访问请求对象,如果视图函数在处理请求时还要访问其他对象,情况会变得更糟.为了避免大量可有可无的参数把视图函数弄得一团糟,Flask使用上下文临时把某些对象变为全局可访问

+ request和response都属于请求上下文对象。
 - 当调用app = Flask(__name__)的时候，创建了程序应用对象app；
 - request 在每次http请求发生时，WSGI server调Flask.call()；然后在Flask内部创建的request对象；
 - app的生命周期大于request，一个app存活期间，可能发生多次http请求，所以就会有多个request。
 - 最终传入视图函数，通过return、redirect或render_template生成response对象，返回给客户端。

###设置cookie

	python
	from flask imoprt Flask,make_response
	@app.route('/cookie')
	def set_cookie():
	    resp = make_response('this is to set cookie')
	    resp.set_cookie('username', 'itcast')
	    return resp

![设置cookie](/images/cookie.png)

session数据的获取

session:请求上下文,用于处理http请求中的一些数据内容
	
	python
	from flask import Flask, session, redirect, url_for, escape, request
	@app.route('/index1')
	def index1():
	    session['username'] = 'itcast'
	    return redirect(url_for('index'))
	@app.route('/')
	def index():
	    return session.get('username')
###应用上下文current_app,g
current_app:应用程序上下文,用于存储应用程序中的变量,可以通过current_app.name打印当前app的名称,也可以在current_app中存储一些变量

应用的启动脚本是哪个文件，启动时指定了哪些参数
加载了哪些配置文件，导入了哪些配置
连了哪个数据库
有哪些public的工具类、常量
应用跑再哪个机器上，IP多少，内存多大

	current_app.name
	current_app.test_value='value'

g作为flask程序全局的一个临时变量,充当者中间媒介的作用,我们可以通过它传递一些数据

	g.name='abc'

## Flask-Script
 通过使用Flask-Script扩展，我们可以在Flask服务器启动的时候，通过命令行的方式传入参数。
 我们可以通过python hello.py runserver --help来查看参数。
 我们还可以通过python hello.py shell进入shell,在命令行中调试代码

 ![命令行](/images/terminator.png)


	python
	from flask import Flask
	from flask_script import Manager
	
	app = Flask(__name__)
	
	manager = Manager(app)
	
	@app.route('/')
	def index():
		return '床前明月光'
	
	if __name__ == "__main__":
		manager.run()


