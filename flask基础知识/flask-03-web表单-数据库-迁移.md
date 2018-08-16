# 1.1 web表单
web表单是web应用程序的基本功能。

它是HTML页面中负责数据采集的部件。表单有三个部分组成：表单标签、表单域、表单按钮。表单允许用户输入数据，负责HTML页面数据采集，通过表单将用户输入的数据提交给服务器。

在Flask中，为了处理web表单，我们一般使用Flask-WTF扩展，它封装了WTForms，并且它有验证表单数据的功能。
### WTForms支持的HTML标准字段
![表单支持的字段](/images/form_field.png) 

### WTForms常用验证函数
![常用验证函数](/images/validate_method.png)

使用Flask-WTF需要配置参数SECRET_KEY。

###在HTML页面中直接写form表单：
	#模板文件
	<form method='post'>
	    <input type="text" name="username" placeholder='Username'>
	    <input type="password" name="password" placeholder='password'>
	    <input type="submit">
	</form>
###视图函数中获取表单数据：

	from flask import Flask,render_template,request
	
	@app.route('/login',methods=['GET','POST'])
	def login():
	    if request.method == 'POST':
	        username = request.form['username']
	        password = request.form['password']
	        print username,password
	    return render_template('login.html',method=request.method)

###使用Flask-WTF实现表单
配置参数:

```
app.config['SECRET_KEY'] = 'silence is gold'
```

模板页面：

	<form method="post">
	    #设置csrf_token
	    {{ form.csrf_token() }}
	    {{ form.us.label }}
	    <p>{{ form.us }}</p>
	    {{ form.ps.label }}
	    <p>{{ form.ps }}</p>
	    {{ form.ps2.label }}
	    <p>{{ form.ps2 }}</p>
	    <p>{{ form.submit() }}</p>
	    {% for x in get_flashed_messages() %}
	        {{ x }}
	    {% endfor %}
 	</form>

视图函数：

	#coding=utf-8
	from flask import Flask,render_template,\
	    redirect,url_for,session,request,flash
	
	#导入wtf扩展的表单类
	from flask_wtf import Form
	#导入自定义表单需要的字段
	from wtforms import SubmitField,StringField,PasswordField
	#导入wtf扩展提供的表单验证器
	from wtforms.validators import DataRequired,EqualTo
	app = Flask(__name__)
	app.config['SECRET_KEY']='1'
	
	#自定义表单类，文本字段、密码字段、提交按钮
	class Login(Form):
	    us = StringField(label=u'用户：',validators=[DataRequired()])
	    ps = PasswordField(label=u'密码',validators=[DataRequired(),EqualTo('ps2','err')])
	    ps2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
	    submit = SubmitField(u'提交')
	
	@app.route('/login')
	def login():
	    return render_template('login.html')
	
	#定义根路由视图函数，生成表单对象，获取表单数据，进行表单数据验证
	@app.route('/',methods=['GET','POST'])
	def index():
	    form = Login()
	    if form.validate_on_submit():
	        name = form.us.data
	        pswd = form.ps.data
	        pswd2 = form.ps2.data
	        print name,pswd,pswd2
	        return redirect(url_for('login'))
	    else:
	        if request.method=='POST':
	            flash(u'信息有误，请重新输入！')
	        print form.validate_on_submit()
	
	    return render_template('index.html',form=form)
	if __name__ == '__main__':
	    app.run(debug=True)

###CSRF攻击原理:
![CSRF攻击原理](/images/csrf_principle.jpg)

CSRF（Cross-site request forgery）跨站请求伪造

图中Browse是浏览器，WebServerA是受信任网站/被攻击网站A，WebServerB是恶意网站/攻击网站B。
（1），一开始用户打开浏览器，访问受信任网站A，输入用户名和密码登陆请求登陆网站A。
（2），网站A验证用户信息，用户信息通过验证后，网站A产生Cookie信息并返回给浏览器。
（3），用户登陆网站A成功后，可以正常请求网站A。
（4），用户未退出网站A之前，在同一浏览器中，打开一个TAB访问网站B。
（5），网站B看到有人访问后，他会返回一些攻击性代码。
（6），浏览器在接受到这些攻击性代码后，促使用户不知情的情况下浏览器携带Cookie（包括sessionId）信息，请求网站A。这种请求有可能更新密码，添加用户什么的操作。

从上面CSRF攻击原理可以看出，要完成一次CSRF攻击，需要被攻击者完成两个步骤：
1，	登陆受信任网站A，并在本地生成COOKIE。
2，	在不登出A的情况下，访问危险网站 B。
看到这里，你也许会说：“如果我不满足以上两个条件中的一个，我就不会受到CSRF的攻击”。是的，确实如此，但你不能保证以下情况不会发生：
1.你不能保证你登录了一个网站后，不再打开一个tab页面并访问另外的网站。
2.你不能保证你关闭浏览器了后，你本地的Cookie立刻过期，你上次的会话已经结束。（事实上，关闭浏览器不能结束一个会话，但大多数人都会错误的认为关闭浏览器就等于退出登录/结束会话了……）
3.上图中所谓的攻击网站，可能是一个存在其他漏洞的可信任的经常被人访问的网站。

在处理 POST 请求之前，flask-wtf 会验证这个请求的 cookie 里的 csrftoken 字段的值和提交的表单里的 csrfmiddlewaretoken 字段的值是否一样。如果一样，则表明这是一个合法的请求，否则，这个请求可能是来自于别人的 csrf 攻击，返回 403 Forbidden

CSRF\_ENABLED是为了CSRF（跨站请求伪造）保护。 SECRET_KEY用来生成加密令牌，当CSRF激活的时候，该设置会根据设置的密匙生成加密令牌。

# 1.2 数据库

知识点

- Flask-SQLALchemy安装
- 连接数据库
- 使用数据库
- 数据库迁移

### 数据库的设置

Web应用中普遍使用的是关系模型的数据库，关系型数据库把所有的数据都存储在表中，表用来给应用的实体建模，表的列数是固定的，行数是可变的。它使用结构化的查询语言。关系型数据库的列定义了表中表示的实体的数据属性。比如：商品表里有name、price、number等。 Flask本身不限定数据库的选择，你可以选择SQL或NOSQL的任何一种。也可以选择更方便的SQLALchemy，类似于Django的ORM。SQLALchemy实际上是对数据库的抽象，让开发者不用直接和数据库打交道，而是通过Python对象来操作数据库，在舍弃一些性能开销的同时，换来的是开发效率的较大提升。

SQLALchemy是一个关系型数据库框架，它提供了高层的ORM和底层的原生数据库的操作。flask-sqlalchemy是一个简化了SQLALchemy操作的flask扩展。

### 安装

```
pip install flask-sqlalchemy
```

如果连接的是mysql数据库,需要安装mysqldb

```
pip install flask-mysqldb
```

### 使用Flask-SQLAlchemy管理数据库

在Flask-SQLAlchemy中，数据库使用URL指定，而且程序使用的数据库必须保存到Flask配置对象的SQLALCHEMY\_DATABASE\_URI键中。

对比下Django和Flask中的数据库设置：

Django的数据库设置：
![Django的数据库设置]()

Flask的数据库设置：
app.config['SQLALCHEMY\_DATABASE\_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'
###常用的SQLAlchemy字段类型
![字段类型]()
###常用的SQLAlchemy列选项
![列选项]()
###常用的SQLAlchemy关系选项
![关系选项]()



#数据库基本操作
在Flask-SQLAlchemy中，插入、修改、删除操作，均由数据库会话管理。会话用db.session表示。在准备把数据写入数据库前，要先将数据添加到会话中然后调用commit()方法提交会话。

在Flask-SQLAlchemy中，查询操作是通过query对象操作数据。最基本的查询是返回表中所有数据，可以通过过滤器进行更精确的数据库查询。

###在视图函数中定义模型类
	from flask import Flask
	from flask_sqlalchemy import SQLAlchemy
	
​	

```
app = Flask(__name__)

#设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/Flask_test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s'% self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    pswd = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s'%self.name
if __name__ == '__main__':
    app.run(debug=True)
```

###模型之前的关联
**一对多**

```python
class Role(db.Model):
    ...
	#关键代码
    us = db.relationship('User', backref='role', lazy='dynamic')
	...

class User(db.Model):
    ...
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

其中realtionship描述了Role和User的关系。在此文中，第一个参数为对应参照的类"User";
第二个参数backref为类User申明新属性的方法；第三个参数lazy决定了什么时候SQLALchemy从数据库中加载数据,如果设置为子查询方式(subquery),则会在加载完User对象后,就立即加载与其关联的对象,这样会让总查询数量减少,但如果返回的条目数量很多,就会比较慢,另外,也可以设置为动态方式(dynamic),这样关联对象会在被使用的时候再进行加载,并且在返回前进行过滤,如果返回的对象数很多,或者未来会变得很多,那最好采用这种方式

**多对多**

```python
registrations = db.Table('registrations',  
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),  
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))  
)  
class Course(db.Model):
	...
class Student(db.Model):
	...
	classes = db.relationship('Course',secondary=registrations,  
                                backref='student',  
                                lazy='dynamic')
```



###常用的SQLAlchemy查询过滤器
![查询过滤器]()
###常用的SQLAlchemy查询执行器
![查询执行器]()

###将数据添加到会话中示例：
	user = User(name='python')
	db.session.add(user)
	db.session.commit()
###创建表：

```
db.create_all()
```

###删除表

```
db.drop_all()
```

###插入一条数据
	ro1 = Role(name='admin')
	db.session.add(ro1)
	db.session.commit()
	#再次插入一条数据
	ro2 = Role(name='user')
	db.session.add(ro2)
	db.session.commit()
###一次插入多条数据
	us1 = User(name='wang',email='wang@163.com',pswd='123456',role_id=ro1.id)
	us2 = User(name='zhang',email='zhang@189.com',pswd='201512',role_id=ro2.id)
	us3 = User(name='chen',email='chen@126.com',pswd='987654',role_id=ro2.id)
	us4 = User(name='zhou',email='zhou@163.com',pswd='456789',role_id=ro1.id)
	db.session.add_all([us1,us2,us3,us4])
	db.session.commit()
###查询:filter_by精确查询
返回名字等于wang的所有人

```
User.query.filter_by(name='wang').all()
```

![过滤名字]()
###first()返回查询到的第一个对象

```
User.query.first()
```

###all()返回查询到的所有对象

```
User.query.all()
```

![查询所有对象]()
###filter模糊查询，返回名字结尾字符为g的所有数据。

```
User.query.filter(User.name.endswith('g')).all()
```

![模糊查询]()
###get():参数为主键，如果主键不存在没有返回内容

```
User.query.get()
```

###逻辑非，返回名字不等于wang的所有数据

```
User.query.filter(User.name!='wang').all()
```

![逻辑非]()
###逻辑与，需要导入and，返回and()条件满足的所有数据
	from sqlalchemy import and_
	User.query.filter(and_(User.name!='wang',User.email.endswith('163.com'))).all()
![逻辑与]()
###逻辑或，需要导入or_
	from sqlalchemy import or_
	User.query.filter(or_(User.name!='wang',User.email.endswith('163.com'))).all()
![逻辑或]()
###not_ 相当于取反
	from sqlalchemy import not_
	User.query.filter(not_(User.name=='chen')).all()
![取反]()
###查询数据后删除
	user = User.query.first()
	db.session.delete(user)
	db.session.commit()
	User.query.all()
###更新数据
	user = User.query.first()
	user.name = 'dong'
	db.session.commit()
	User.query.first()
![更新数据]()
###关联查询示例：角色和用户的关系是一对多的关系，一个角色可以有多个用户，一个用户只能属于一个角色。
查询角色的所有用户

```
#查询roles表id为1的角色
ro1 = Role.query.get(1)
#查询该角色的所有用户
ro1.us.all()
```

![查询角色的所有用户]()
查询用户所属角色

```
#查询users表id为3的用户
us1 = User.query.get(3)
#查询用户属于什么角色
us1.role
```

![查询用户所属角色]()

# 1.4 综合案例(图书管理)

###定义模型
模型表示程序使用的数据实体，在Flask-SQLAlchemy中，模型一般是Python类，继承自db.Model，db是SQLAlchemy类的实例，代表程序使用的数据库。

类中的属性对应数据库表中的列。id为主键，是由Flask-SQLAlchemy管理。db.Column类构造函数的第一个参数是数据库列和模型属性类型。

注:向数据库中插入中文后,会报错,需要修改数据库的编码集:

```
alter database 数据库名 CHARACTER SET utf8
```

如下示例：定义了两个模型类，作者和书名。

```
#coding=utf-8
from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#设置连接数据
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#实例化SQLAlchemy对象
db = SQLAlchemy(app)

#定义模型类-作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
    email = db.Column(db.String(64))
    au_book = db.relationship('Book',backref='author')
    def __str__(self):
        return 'Author:%s' %self.name

#定义模型类-书名
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key=True)
    info = db.Column(db.String(32),unique=True)
    lead = db.Column(db.String(32))
    au_book = db.Column(db.Integer,db.ForeignKey('author.id'))
    def __str__(self):
        return 'Book:%s,%s'%(self.info,self.lead)
```

###创建表
![创建表]()
###查看author表结构 desc author
![author表结构]()
###查看books表结构 desc books
![books表结构]()

```
#coding=utf-8
from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/test1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='s'

db = SQLAlchemy(app)

#创建表单类，用来添加信息
class Append(Form):
    au_info = StringField(validators=[DataRequired()])
    bk_info = StringField(validators=[DataRequired()])
    submit = SubmitField(u'添加')
```

​	

```
@app.route('/',methods=['GET','POST'])
def index():
    author = Author.query.all()
    book = Book.query.all()
    form = Append()
    if form.validate_on_submit():
        #获取表单输入数据
        wtf_au = form.au_info.data
        wtf_bk = form.bk_info.data
        #把表单数据存入模型类
        db_au = Author(name=wtf_au)
        db_bk = Book(info=wtf_bk)
        db.session.add_all([db_au,db_bk])
        db.session.commit()
        author = Author.query.all()
        book = Book.query.all()
        return render_template('index.html',author=author,book=book,form=form)
    else:
        if request.method=='POST':
        	flash(u'输入错误，请重新输入')
    return render_template('index.html',author=author,book=book,form=form)

#删除作者
@app.route('/delete_author<id>')
def delete_author(id):
    au = Author.query.filter_by(id=id).first()
    db.session.delete(au)
    return redirect(url_for('index'))

#删除书名
@app.route('/delete_book<id>')
def delete_book(id):
    bk = Book.query.filter_by(id=id).first()
    db.session.delete(bk)
    return redirect(url_for('index'))
```

​	

```
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    #生成数据
    au_xi = Author(name='我吃西红柿',email='xihongshi@163.com')
    au_qian = Author(name='萧潜',email='xiaoqian@126.com')
    au_san = Author(name='唐家三少',email='sanshao@163.com')
    bk_xi = Book(info='吞噬星空',lead='罗峰')
    bk_xi2 = Book(info='寸芒',lead='李杨')
    bk_qian = Book(info='飘渺之旅',lead='李强')
    bk_san = Book(info='冰火魔厨',lead='融念冰')
    #把数据提交给用户会话
    db.session.add_all([au_xi,au_qian,au_san,bk_xi,bk_xi2,bk_qian,bk_san])
    #提交会话
    db.session.commit()
    app.run(debug=True)
```

###生成数据后，查看数据：
![生成数据]()
###模板页面示例：

```
<h1>玄幻系列</h1>
<form method="post">
    {{ form.csrf_token }}
    <p>作者：{{ form.au_info }}</p>
    <p>书名：{{ form.bk_info }}</p>
    <p>{{ form.submit }}</p>
</form>
{% for message in get_flashed_messages() %}
	{{ message }}
{% endfor %}
<ul>
    <li>{% for x in author %}</li>
    <li>{{ x }}</li><a href='/delete_author{{ x.id }}'>删除</a>
    <li>{% endfor %}</li>
</ul>
<hr>
<ul>
    <li>{% for x in book %}</li>
    <li>{{ x }}</li><a href='/delete_book{{ x.id }}'>删除</a>
    <li>{% endfor %}</li>
</ul>
```

###添加数据后，查看数据：
![添加数据]()

# 1.5 数据库迁移

在开发过程中，需要修改数据库模型，而且还要在修改之后更新数据库。最直接的方式就是删除旧表，但这样会丢失数据。

更好的解决办法是使用数据库迁移框架，它可以追踪数据库模式的变化，然后把变动应用到数据库中。

在Flask中可以使用Flask-Migrate扩展，来实现数据迁移。并且集成到Flask-Script中，所有操作通过命令就能完成。

为了导出数据库迁移命令，Flask-Migrate提供了一个MigrateCommand类，可以附加到flask-script的manager对象上。

首先要在虚拟环境中安装Flask-Migrate。

```
pip install flask-migrate
```

###创建迁移仓库

```
#这个命令会创建migrations文件夹，所有迁移文件都放在里面。
python database.py db init
```

![创建迁移仓库]()

###创建迁移脚本
自动创建迁移脚本有两个函数，upgrade()函数把迁移中的改动应用到数据库中。downgrade()函数则将改动删除。自动创建的迁移脚本会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。对比不一定完全正确，有可能会遗漏一些细节，需要进行检查

```
#创建自动迁移脚本
python database.py db migrate -m 'initial migration'
```

![创建迁移脚本]()
###更新数据库

```
python database.py db upgrade
```

```
#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app = Flask(__name__)
manager = Manager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/Flask_test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app,db) 

#manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db',MigrateCommand)

#定义模型Role
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串，
    def __repr__(self):
        return 'Role:'.format(self.name)

#定义用户
class User(db.Model):
    __talbe__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #设置外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:'.format(self.username)
```

​	

```
if __name__ == '__main__':
    manager.run()
```

###返回以前的版本
可以根据history命令找到版本号,然后传给downgrade命令:

```
python app.py db history
```

<base> ->  版本号 (head), initial migration

```
python app.py db downgrade 版本号
```

###实际操作顺序:

- 1,python 文件 db init
- 2,python 文件 db migrate -m"版本名"
- 3,python 文件 db upgrade 然后观察表结构
- 4,根据需求修改模型
- 5,python 文件 db migrate -m"新版本名" 
- 6,python 文件 db upgrade 然后观察表结构
- 7,若返回版本,则利用 python 文件 db history查看版本号
- 8,python 文件 db downgrade 版本号

