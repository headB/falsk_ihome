# 2.1 邮件扩展

在开发过程中，很多应用程序都需要通过邮件提醒用户，Flask的扩展包Flask-Mail通过包装了Python内置的smtplib包，可以用在Flask程序中发送邮件。

Flask-Mail连接到简单邮件协议（Simple Mail Transfer Protocol,SMTP）服务器，并把邮件交给服务器发送。
###设置邮箱授权码
![设置授权码](/images/identify_code.png)

如下示例，通过开启QQ邮箱SMTP服务设置，发送邮件。

```
#coding:utf-8
from flask import Flask,render_template
from flask_mail import Mail, Message
from threading import Thread
```

​	

```
app = Flask(__name__)
# 配置邮件：服务器／端口／安全套接字层／邮箱名／授权码
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ccyznhy'
app.config['MAIL_PASSWORD'] = '111qqq'
app.config['MY_MAIL_SENDER'] = 'Flasky Admin123<ccyznhy@126.com>'
app.config['MY_MAIL_TO'] = '939064936@qq.com'

mail = Mail(app)
```

​	

```
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
```

​	

```
def send_email(to, subject):
    msg = Message(subject,sender=app.config['MY_MAIL_SENDER'], recipients=[to])
    msg.body = 'msg body'
    # msg.html = '<h1>html数据</h1>'
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
```

​	

```
@app.route('/')
def index():
    send_email(app.config['MY_MAIL_TO'], 'New User')
    return "Sent　Succeed"

if __name__ == "__main__":
    app.run()
```

# 2.2 综合案例

需求:
在表单中提交输入内容,如果是第一次输入,则显示陌生人,并提示"第一次见到你",否则显示输入内容,并提示"很高兴再次见到你"

屏幕下方显示本地时间
效果图如下:
![案例效果图](/images/demo_result.png)

###案例分析:

- 1,界面需要用到模板相关知识,如果需要快速实现,可以继承已有的flask-bootstrap扩展中的模板
- 2,表单使用flask-wtf相关知识
- 3,记录数据使用flask-sqlalchemy相关知识

###数据库处理
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'hard to guess string'
	app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:mysql@127.0.0.1:3306/test'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	

```
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

​	

```
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
```

​	

```
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

#为数据库添加上下文信息,使得进入shell后,无需导入app,db,User,Role这些对象
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    manager.run()
```

###界面处理
base.html

```
{% extends "bootstrap/base.html" %}

{% block title %}Demo{% endblock %}

{% block head %}
{{ super() }}
{% endblock %}
{# 顶部内容 #}
{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Demo</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">主页</a></li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}
{# 内容部分 #}
{% block content %}
<div class="container">
    {% for message in get_flashed_messages() %}
    <div class="alert alert-warning">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        {{ message }}
    </div>
    {% endfor %}

    {% block page_content %}{% endblock %}
</div>
{% endblock %}
{# 时间显示 #}
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
```

index.html

```
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Demo{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>你好, {% if name %}{{ name }}{% else %}陌生人{% endif %}!</h1>
    {% if not known %}
    <p>第一次见到你</p>
    {% else %}
    <p>很高兴再次见到你</p>
    {% endif %}

{{ wtf.quick_form(form) }}
<br/>
<p>当前时间为： {{ moment(current_time).format('LLLL') }}.</p>
</div>
{% endblock %}
```

404.html

```
{% extends "base.html" %}

{% block title %}页面没有找到{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Not Found</h1>
</div>
{% endblock %}
```

500.html

```
{% extends "base.html" %}

{% block title %}服务器搬家了{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Internal Server Error</h1>
</div>
{% endblock %}
```

###表单处理
	class NameForm(FlaskForm):
	    name = StringField(u'你叫什么名字？', validators=[DataRequired()])
	    submit = SubmitField('Submit')

###表单验证

```python
@app.route('/', methods=['GET', 'POST'])

	def index():
	    form = NameForm()
	    if form.validate_on_submit():
	        user = User.query.filter_by(username=form.name.data).first()
	        if user is None:

	            user = User(username=form.name.data)

	            db.session.add(user)

	            session['known'] = False

	        else:

	            session['known'] = True

	        session['name'] = form.name.data

	        return redirect(url_for('index'))

	    return render_template('index.html', form=form, name=session.get('name'),

	                           known=session.get('known', False),current_time=datetime.utcnow())



```

​	2.3 控制代码块

###if语句
Jinjia语法中的if语句跟Python中的if语句相似,后面的布尔值或返回布尔值的表达式将决定代码中的哪个流程会被执行:

```
{%if user.is_logged_in() %}
	<a href='/logout'>Logout</a>
{% else %}
	<a href='/login'>Login</a>
{% endif %}
```

过滤器可以被用在if语句中:

```
{% if comments | length > 0 %}
	There are {{ comments | length }} comments
{% else %}
	There are no comments
{% endif %}
```

###循环
我们可以在Jinjia中使用循环来迭代任何列表或者生成器函数

```
{% for post in posts %}
	<div>
		<h1>{{ post.title }}</h1>
		<p>{{ post.text | safe }}</p>
	</div>
{% endfor %}
```

循环和if语句可以组合使用,以模拟Python循环中的break功能,下面这个循环将只会渲染post.text不为None的那些post:
	{% for post in posts if post.text %}
		<div>
			<h1>{{ post.title }}</h1>
			<p>{{ post.text | safe }}</p>
		</div>
	{% endfor %}

在循环内部,你可以使用一个叫做loop的特殊变量来获得关于for循环的一些信息,比如,要是我们想知道当前被迭代的元素序号,并模拟Python中的enumerate函数做的事情,则可以使用loop变量的index属性,例如:

```
{% for post in posts%}
	{{loop.index}}. {{post.title}}
{% endfor %}
```

会生成这样的结果:

1,Post title

2,Second Post

cycle函数会在每次循环的时候,返回其参数中的下一个元素,可以拿上面的例子来说明:

```
{% for post in posts%}
	{{loop.cycle('odd','even')}} {{post.title}}
{% endfor %}
```

会输出这样的结果:

odd Post Title

even Second Post

###宏
对宏(macro)最合适的理解是把它看作Jinjia中的一个函数,它会返回一个模板或者HTML字符串,为了避免反复地编写同样的模板代码,可以把他们写成函数以进行重用,例如:下面的宏可以在你的模板中添加一个带有label标签且使用Bootstrap css的输入框

```
{% macro input(name,label,value='',type='text') %}
	<div class="form-group">
		<input type="{{type}}" name="{{name}}"
			value="{{value|escape}}" class="form-control">
	</div>
{% endmacro %}
```

现在你就可以通过调用这个宏,快速的向表单插入一个输入框:
这会输出:
	<div class="form-group">
		<input type="text" name="name"
			value="" class="form-control">
	</div>

把宏单独抽取取来，封装成html文件，其它模板中导入使用

文件名可以自定义macro.html

```
{% macro function() %}
	<div class="form-group">
		<input type="{{type}}" name="{{name}}"
		value="{{value|escape}}" class="form-control">
	</div>
{% endmacro %}
```

在其它模板文件中先导入，再调用

```
{% import 'macro.html' as func %}
{% func.function() %}
```

# 2.4 模板的继承

###基本使用
模板继承是为了重用模板中的公共内容。{% block head %}标签定义的元素可以在衍生模板中修改，extends指令声明这个模板继承自哪,父模板中定义的块在子模板中被重新定义，在子模板中调用父模板的内容可以使用super()。a

```
{% extends 'base.html' %}
{% block content %}
	...
{% endblock %}
```

###综合案例

通过访问url,显示不同的网页内容(见代码附件)

# 2.5 Flask特有的变量和函数

你可以在自己的模板中访问一些Flask默认内置的函数和对象

**config**

你可以从模板中直接访问Flask当前的config对象:

```
{{config.SQLALCHEMY_DATABASE_URI}}
sqlite:///database.db
```

**request**

就是flask中代表当前请求的request对象:

```
{{request.url}}
http://127.0.0.1
```

**session**

为Flask的session对象

```
{{session.new}}
True
```

**url_for()**

url\_for会根据传入的路由器函数名,返回该路由对应的URL,在模板中始终使用url_for()就可以安全的修改路由绑定的URL,则不比担心模板中渲染出错的链接:

```
{{url_for('home')}}
/
```

如果我们定义的路由URL是带有参数的,则可以把它们作为关键字参数传入url_for(),Flask
会把他们填充进最终生成的URL中:

```
{{ url_for('post', post_id=1)}}
/post/1
```

**get\_flashed\_messages()**

这个函数会返回之前在flask中通过flask()传入的消息的列表,flash函数的作用很简单,可以把由Python字符串表示的消息加入一个消息队列中,再使用get\_flashed\_message函数取出它们并消费掉:

```
{%for message in get_flashed_messages()%}
	{{message}}
{%endfor%}
```

