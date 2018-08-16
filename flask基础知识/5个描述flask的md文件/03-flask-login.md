# 1.3 Flask-Login
###Flask-Login简介
Flask-Login扩展可以快速实现登陆注册功能
###密码安全性处理
在登陆时,需要设置和使用密码,但开发中数据库存储密码一般不是明文存储,而是密文存储,我们在用户提交密码时,需要对密码进行加密处理,然后将加密后的密码进行进行存储,我们对数据库的加密方式为散列加密,如下所示:

**使用Werkzeug实现密码散列**

- generate\_password\_hash(password,method=pbkdf2:sha1,salt\_length=8):这个函数将
原始密码作为输入,以字符串形式输出密码的散列值,输出的值可保存在用户数据库中。
method和salt_length的默认值就能满足大多数需求。
- check\_password_hash(hash, password):这个函数的参数是从数据库中取回的密码散列值和用户输入的密码。返回值为True表明密码正确。
修改User模型,加入密码散列:

#
	
	class User(db.Model):
	    __tablename__ = 'users'
	    id = db.Column(db.Integer, primary_key=True)
	    email = db.Column(db.String(64), unique=True, index=True)
	    username = db.Column(db.String(64), unique=True, index=True)
	    password_hash = db.Column(db.String(128))
	
	    @property
	    def password(self):
	        raise AttributeError('password is not a readable attribute')
	
	    @password.setter
	    def password(self, password):
	        self.password_hash = generate_password_hash(password)
	
	    def verify_password(self, password):
	        return check_password_hash(self.password_hash, password)
	
	    def __repr__(self):
	        return '<User %r>' % self.username

计算密码散列值的函数通过名为password的只写属性实现。设定这个属性的值时,赋值方法会调用Werkzeug提供的generate\_password\_hash()函数,并把得到的结果赋值给password_hash 字段。如果试图读取password属性的值,则会返回错误,原因很明显,因为生成散列值后就无法还原成原来的密码了

verify\_password方法接受一个参数(即密 码), 将其传给Werkzeug提供的check\_password\_hash()函数,和存储在User模型中的密码散列值进行比对。如果这个方法返回True,就表明密码是正确的

使用密码散列的好处为:两个用户使用相同的密码,但密码散列值也完全不一样
###创建蓝图
由于注册登陆模块是一个独立的较大的模块,则我们创建一个独立的目录用于登陆注册功能的代码实现
代码:
__init__.py文件代码:

	from flask import Blueprint
	auth = Blueprint('auth', __name__)
	from . import views
views.py文件代码:

	from flask import render_template
	from . import auth
	@auth.route('/login')
	def login():
		return render_template('auth/login.html')
注:为了方便管理,登陆所需要的模版文件保存在auth文件夹中,这个文件夹在app/templates中创建

注册蓝图:

	def create_app(config_name):
	# ...
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	return app
###使用Flask-Login认证用户
Flask-Login是个非常有用的小型扩展,专门用于管理用户认证系统中的认证状态,且不依赖特定的认证机制
###Flask-Login要求实现的用户方法

- is_authenticated() 如果用户已经登录,必须返回 True ,否则返回 False
- is_active() 如果允许用户登录,必须返回 True ,否则返回 False 。如果要禁用账户,可以返回 False
- is_anonymous() 对普通用户必须返回 False
- get_id() 必须返回用户的唯一标识符,使用 Unicode 编码字符串
这些方法在模型类中需要实现,而flask-login提供了一个UserMixin类,已经默认实现了这四个方法,且满足大部分需求,所以,我们的User模型需要继承UserMixin类

```
class User(UserMixin, db.Model):
```
###初始化Flask-Login
	from flask_login import LoginManager
	login_manager = LoginManager()
	login_manager.session_protection = 'strong'
	login_manager.login_view = 'auth.login'
	def create_app(config_name):
		# ...
		login_manager.init_app(app)
		# ...
LoginManager对象的session\_protection属性可以设为 None、'basic'或'strong',以提供不同的安全等级防止用户会话遭篡改。设为'strong'时,Flask-Login会记录客户端IP地址和浏览器的用户代理信息,如果发现异动就登出用户。login_view属性设置登录页面的端点。Flask-Login要求实现一个回调函数,使用指定的标识符加载用户,这个函数需要定义在models.py文件中

	from . import login_manager
	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))
加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户,这
个函数必须返回用户对象;否则应该返回None

##登入登出功能的实现
###表单的处理
用户的登录表单中包含一个用于输入电子邮件地址的文本字段、一个密码字段、一个"记住我"复选框和提交按钮

	class LoginForm(FlaskForm):
	    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
	                                             Email()])
	    password = PasswordField(u'密码', validators=[Required()])
	    remember_me = BooleanField(u'记住我')
	    submit = SubmitField(u'登陆')
###表单验证
	@auth.route('/login', methods=['GET', 'POST'])
	def login():
	    form = LoginForm()
	    if form.validate_on_submit():
	        user = User.query.filter_by(email=form.email.data).first()
	        if user is not None and user.verify_password(form.password.data):
	            login_user(user, form.remember_me.data)
	            return redirect(request.args.get('next') or url_for('main.index'))
	        flash(u'用户名或密码错误')
	    return render_template('auth/login.html', form=form)

	@auth.route('/logout')
	@login_required
	def logout():
	    logout_user()
	    flash(u'成功注销用户')
	    return redirect(url_for('main.index'))
其中:被login_required装饰器装饰过的路由函数只允许在登陆后才能访问
##注册功能的实现
###表单的处理

	class RegistrationForm(FlaskForm):
	    email = StringField('Email', validators=[Required(), Length(1, 64),
	                                           Email()])
	    username = StringField(u'用户名', validators=[
	        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
	                                          '用户名只能包含字母,数字,点或下划')])
	    password = PasswordField(u'密码', validators=[
	        Required(), EqualTo('password2', message='两次密码输入不一致')])
	    password2 = PasswordField(u'确认密码', validators=[Required()])
	    submit = SubmitField(u'注册')
	
	    def validate_email(self, field):
	        if User.query.filter_by(email=field.data).first():
	            raise ValidationError('当前邮箱已经被注册过了')
	
	    def validate_username(self, field):
	        if User.query.filter_by(username=field.data).first():
	            raise ValidationError('当前用户名已经被占用')
这个表单使用WTForms提供的Regexp 验证函数,确保username字段只包含字母、数字、下划线和点号。这个验证函数中正则表达式后面的两个参数分别是正则表达式的旗标和验证失败时显示的错误消息。安全起见,密码要输入两次。此时要验证两个密码字段中的值是否一致,这种验证可使用WTForms 提供的另一验证函数实现,即EqualTo。个验证函数要附属到两个密码字段中的一个上,另一个字段则作为参数传入。这个表单还有两个自定义的验证函数,以方法的形式实现。如果表单类中定义了以validate_ 开头且后面跟着字段名的方法,这个方法就和常规的验证函数一起调用。本例分别为email和username字段定义了验证函数,确保填写的值在数据库中没出现过。自定义的验证函数要想表示验证失败,可以抛出ValidationError异常,其参数就是错误消息
###表单验证

	@auth.route('/register', methods=['GET', 'POST'])
	def register():
	    form = RegistrationForm()
	    if form.validate_on_submit():
	        user = User(email=form.email.data,
	                    username=form.username.data,
	                    password=form.password.data)
	        db.session.add(user)
	        db.session.commit()
	        flash('现在可以登陆了')
	        return redirect(url_for('auth.login'))
	    return render_template('auth/register.html', form=form)
