# 2.1 模版
### 模版
###知识点

- 模板使用
- 变量
- 过滤器
- web表单
- 控制语句
- 宏与继承
- Flask中的特殊变量和方法

在flask中,内置了一个模版语言,称之为Jinjia2,它是由Python实现的模版语言.

模版语言是一种被设计来自动生成文档的简单文本格式,在模版语言中,一般都会把一些变量传给模版,替换模版的特定位置上预先定义好的占位变量名

在Jinjia中,变量名是由{{}}来表示的,这种{{}}语法叫做变量代码块,另外还有用{% %}定义的控制代码块,可以实现一些语言层次的功能,比如循环或者if语句

例子:
	<h1>{{ post.title }}</h1>

Jinjia模版中的变量代码块可以是任意Python类型或者对象,只要它能够被Python的str()方法转换为一个字符串就可以,比如,可以通过下面的方式显示一个字典或者列表中的某个元素:
	
	{{your_dict['key']}}
	{{your_list[0]}}
# 2.2 过滤器

一种常见的错误观点是,Jinjia和Python差不多,因此它们看起来很像,但其实Jinjia和Python有很多不同之处,在jinjia中一些常用的Python函数其实并不存在,在Jinjia中可以把变量传给一些内建的函数来进行某些修改,以满足显示的需要,这些函数叫做过滤器(filter),在变量代码块中使用管道操作符|可以调用它们

``` 
{{variable | filter_name(*args)}}
```

如果没有任何参数传给过滤器,则可以把括号省略掉

```
{{variable | filter_name}}
```

过滤器也可以在控制代码块中调用,这样就可以对一整块文字应用这个过滤器:

	{% filter filter_name %}
		一大堆文字
	{% endfilter %}

**default**

变量在为假值的时候被替换成默认值,把传给default的第2个参数设为True:

```
{{'' | default{'An empty string', True}}}
```

**float**

可使用Python的float()方法将传入只转换为浮点数显示:

```
{{75|float}}
```

**int**

可使用Python的int()方法将传入值转换为整数显示:

```
{{12.5|int}}
```

**join**

这个过滤器会把列表拼成一个字符串,与list的同名方法的作用完全一样

```
{{['Python','SQL'] |join(',')}}
```

**length**

这个过滤器扮演了与Python中的len()方法同样的角色

```
{{post.tags|length}}
```

**round**

它会把一个浮点数转换到给定的小数位数

```
{{3.1415926 | round(1)}}
```

你还可以指定如何转换:

	{{4.8 | round(1,"common")}}
	{{4.2 | round(1,"common")}}
	{{4.8 | round(1,"floor")}}
	{{4.2 | round(1,"ceil")}}

common代表的方式就跟我们在生活中做的一样:对多位数进行四舍五入,floor则总是把位数直接截断,ceil总是会向上取整,不论后面的小数是多少

**safe**

如果你向直接把HTML作为变量插入页面中,比如在想显示一部分内容的时候,Jinjia会自动尝试对输出进行HTML转义

```
{{"<h1>test content</h1>"}}
```

这是必要的安全措施,如果应用某个输入接口允许用户提交任何文本,那么恶意用户也可以用它来提交HTML代码,比如,一名用户在恢复狂里提交了含有script标签的文本,如果Jinjia没有转义功能,那么访问这个页面的所有浏览器都会执行这个标签中的脚本

但是,我们仍然需要一种方式,对安全的HTML不转义且直接显示,例如我们当然能确保HTML内容是安全的,这样可以用safe来实现

```
{{"<h1>test content</h1>" | safe}}
```

**title**

可以把字符串中单词的手自缚改为大写格式:

```
{{"test content" | title}}
```

**tojson**

可以用这种方式调用Python的json.dumps函数来序列化对象,需要确保传过去的对象是被json模块序列化的:

```
{{ {'key':False, 'key2':None , 'key3': 45} | tojson}}
```

**trucate**

用于接收一个长字符串,返回一个截断成指定长度的字符串,并添加省略号:

```
{{"test content test content test content test content" | truncate(10)}}
```

在缺省状态下,任何从中间被截断的单词会被丢弃掉,如果不想这样,则可以传一个额外的参数值True:

```
{{"test content test content test content test content" | truncate(10,True)}}
```

**capitalize**

把变量值的首字母转成大写，其余字母转小写

```
{{ 'hello' | capitalize }}
```

**lower**

把值转成小写

```
{{ 'HELLO' | lower }}
```

**upper**

把值转成大写

```
{{ 'hello' | upper }}
```

**trim**

把值的首尾空格去掉

```
{{ ' hello world ' | trim }}
```

**format**

格式化输出

```
{{ '%s is %d' | format('name',17) }}
```

**striptags**

渲染之前把值中所有的HTML标签都删掉

```
{{ '<em>hello</em>' | striptags }}
```



自定义过滤器

在Jinjia中增加一个过滤器非常简单,就跟在Python中写一个函数一样,我们可以通过一个例子来理解过滤器的原理,下面这个简单的过滤器计算一个子字符串在元字符串中出现的次数,并且将其返回,调用方式是:

```
{{variable | filter_name("string")}}
```

因此我们可以这样定义过滤器函数:

	def count_substring(string, sub):
		return string.count(sub)
我们需要在main.py文件中手动地把它加入到jia_env对象的filter字典,以使该函数可作为过滤器被调用:

```
app.jinjia_env.filters['count_substring'] = count_substring
```

**注释**

模板中的注释使用{# #}来定义,不会出现在生成的HTML中,例如:
	{# 我是注释 #}

# 2.3 控制代码块

###if语句
Jinjia语法中的if语句跟Python中的if语句相似,后面的布尔值或返回布尔值的表达式将决定代码中的哪个流程会被执行:

	{%if user.is_logged_in() %}
		<a href='/logout'>Logout</a>
	{% else %}
		<a href='/login'>Login</a>
	{% endif %}

过滤器可以被用在if语句中:

	{% if comments | length > 0 %}
		There are {{ comments | length }} comments
	{% else %}
		There are no comments
	{% endif %}

###循环
我们可以在Jinjia中使用循环来迭代任何列表或者生成器函数

	{% for post in posts %}
		<div>
			<h1>{{ post.title }}</h1>
			<p>{{ post.text | safe }}</p>
		</div>
	{% endfor %}

循环和if语句可以组合使用,以模拟Python循环中的break功能,下面这个循环将只会渲染post.text不为None的那些post:
	{% for post in posts if post.text %}
		<div>
			<h1>{{ post.title }}</h1>
			<p>{{ post.text | safe }}</p>
		</div>
	{% endfor %}

在循环内部,你可以使用一个叫做loop的特殊变量来获得关于for循环的一些信息,比如,要是我们想知道当前被迭代的元素序号,并模拟Python中的enumerate函数做的事情,则可以使用loop变量的index属性,例如:

	{% for post in posts%}
		{{loop.index}}. {{post.title}}
	{% endfor %}

会生成这样的结果:

1,Post title

2,Second Post

cycle函数会在每次循环的时候,返回其参数中的下一个元素,可以拿上面的例子来说明:

	{% for post in posts%}
		{{loop.cycle('odd','even')}} {{post.title}}
	{% endfor %}
会输出这样的结果:

odd Post Title

even Second Post

###宏
对宏(macro)最合适的理解是把它看作Jinjia中的一个函数,它会返回一个模板或者HTML字符串,为了避免反复地编写同样的模板代码,可以把他们写成函数以进行重用,例如:下面的宏可以在你的模板中添加一个带有label标签且使用Bootstrap css的输入框

	{% macro input(name,label,value='',type='text') %}
		<div class="form-group">
			<input type="{{type}}" name="{{name}}"
				value="{{value|escape}}" class="form-control">
		</div>
	{% endmacro %}
现在你就可以通过调用这个宏,快速的向表单插入一个输入框:
这会输出:
	<div class="form-group">
		<input type="text" name="name"
			value="" class="form-control">
	</div>

把宏单独抽取取来，封装成html文件，其它模板中导入使用

文件名可以自定义macro.html

	{% macro function() %}
		<div class="form-group">
			<input type="{{type}}" name="{{name}}"
			value="{{value|escape}}" class="form-control">
		</div>
	{% endmacro %}
在其它模板文件中先导入，再调用

	{% import 'macro.html' as func %}
	{% func.function() %}


# 2.4 模板的继承

###基本使用
模板继承是为了重用模板中的公共内容。{% block head %}标签定义的元素可以在衍生模板中修改，extends指令声明这个模板继承自哪,父模板中定义的块在子模板中被重新定义，在子模板中调用父模板的内容可以使用super()。

	{% extends 'base.html' %}
	{% block content %}
		...
	{% endblock %}

###综合案例

通过访问url,显示不同的网页内容(见代码附件)

# 2.5 Flask特有的变量和函数
你可以在自己的模板中访问一些Flask默认内置的函数和对象

**config**

你可以从模板中直接访问Flask当前的config对象:

	{{config.SQLALCHEMY_DATABASE_URI}}
	sqlite:///database.db

**request**

就是flask中代表当前请求的request对象:

	{{request.url}}
	http://127.0.0.1

**session**

为Flask的session对象

	{{session.new}}
	True

**url_for()**

url\_for会根据传入的路由器函数名,返回该路由对应的URL,在模板中始终使用url_for()就可以安全的修改路由绑定的URL,则不比担心模板中渲染出错的链接:

	{{url_for('home')}}
	/
如果我们定义的路由URL是带有参数的,则可以把它们作为关键字参数传入url_for(),Flask
会把他们填充进最终生成的URL中:

	{{ url_for('post', post_id=1)}}
	/post/1

**get\_flashed\_messages()**

这个函数会返回之前在flask中通过flask()传入的消息的列表,flash函数的作用很简单,可以把由Python字符串表示的消息加入一个消息队列中,再使用get\_flashed\_message函数取出它们并消费掉:

	{%for message in get_flashed_messages()%}
		{{message}}
	{%endfor%}



