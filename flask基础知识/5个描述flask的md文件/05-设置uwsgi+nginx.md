# 1.5 利用uwsgi和nginx进行服务器部署
###阿里云服务器
- 1,选择云服务器:阿里云服务器
- 2,购买服务器:在首页最底下有一个免费使用的优惠购买:最便宜的套餐为9.9元,送一个入门级别的云服务器ECS和其他的一些服务器
- 3,购买后,再次进入首页最底下,点击免费获取
![免费获取1](/images/free_get1.png)
- 4,进入如下图所示的界面,点击第一项云服务器ECS的立即开通(由于本人已经创建,故:没有显示立即开通,而是前往控制台).注:创建服务器选择ubuntu16.04 64位的操作系统
![免费获取2](/images/free_get2.png)
![创建服务器](/images/server_create.png)
- 4,进入控制台,查看实例创建情况
![控制台](/images/instance.png)
- 5,利用命令行进行远程服务器登陆

打开本地的ubuntu系统,通过ssh命令进行登陆	

```
ssh 用户名@ip地址
```
```
输入密码:xxxx
```

##登陆后的相关软件安装
###python和pip
这两个环境是ubuntu16.04自带的
###uwsgi安装
uwsgi是一个能够运行flask项目的高性能web服务器
需要先安装两个依赖

```
apt-get install build-essential python-dev
```
然后进行uwsgi的安装

```
pip install uwsgi
```
###nginx安装
通过指令进行安装

```
apt-get install nginx
```
###hello world程序的部署
1,利用pycharm创建python项目
2,利用scp命令将整个项目上传到远程服务器中

在本地目录下输入指令:

```
scp -r 本地目录 用户名@ip地址:远程目录
```
3,创建config.ini文件作为uwsgi的初始化配置文件
	
	[uwsgi]				#需要声明uwsgi使得uwsgi能够识别当前文件
	master = true
	socket = :5000		#如果单纯运行uwsgi文件则使用http,如果和nginx配合,则使用socket
	processes = 4		#设定进程数
	threads = 2			#设定线程数
	wsgi-file = app.py 	#指定运行的文件
	chdir = /home/hello	#指定运行的项目的目录
	callable = app		#指定运行的实例
	buffer-size = 32768	#指定uwsgi服务器的缓冲大小
4,通过指令运行uwsgi.ini服务器

```
uwsgi --ini config.ini -d uwsgi.log
```

其中
--ini config.ini 表示指定运行的配置文件

-d uwsgi.log 表示uwsgi在后台运行,运行过程中产生的日志会存储在uwsgi.log中

5,配置nginx服务器

编辑文件:/etc/nginx-sites-available/default

修改为如下内容:
server {

	listen 80 default_server;

	server_name 59.110.240.237;	

	location / {
		include uwsgi_params;
		uwsgi_pass 59.110.240.237:5000;
		uwsgi_read_timeout 100;
	}

}

将server中原有的,上述配置中不能存在的内容注释或删除掉

6,启动和停止nginx服务器

```
/etc/init.d/nginx start
```

```
/etc/init.d/nginx stop
```
###本地项目的远程部署
软件的安装:

mysql的安装:


```
apt-get install mysql-server
```

```
apt-get install libmysqlclient-dev
```


虚拟环境的安装

virtualenv和virtualenvwrapper的安装:

```
pip install virutalenv
```

```
pip install virutalenvwrapper
```

使得安装的virtualenvwrapper生效:

- 1,编辑~/.bashrc文件

内容如下:

	export WORKON_HOME=$HOME/.virtualenvs
	export PROJECT_HOME=$HOME/workspace
	source /usr/local/bin/virtualenvwrapper.sh

- 2,使编辑后的文件生效

```
source ~/.bashrc
```

- 3,创建虚拟环境

```
mkvirtualenv 虚拟环境名称
```

- 4,在虚拟环境中安装项目所需要的依赖

```
pip install -r 依赖文件(requirements.txt)
```

- 5,通过scp命令将整个项目上传到远程服务器
- 6,创建config.ini文件,配置和之前一致,但要加入一个虚拟环境的配置

```
pythonpath = /root/.virtualenvs/flask_test/lib/python2.7/site-packages #表示指定虚拟环境目录,使用虚拟环境中安装的扩展
```

- 7,运行uwsgi和之前操作一致,但要修改项目目录
- 8,运行nginx和之前操作一致,但要修改项目目录