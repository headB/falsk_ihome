# celery模型说明
1. 发送短信,可能会发生堵塞
2. 安装`pip install -U celery
3. 任务队列
    1. rabbitMQ
    2. MessageQueue
    3. redis
4. celery结构
    1. 客户端(发布任务的一方,例如是django,flask)
    2. 任务处理者(worker,多进程,协程,gevent,greenlet)-具备多任务处理
    3. 任务队列(broker)
    4. 还可以有一个第四方,专门用来存放数据(backend)
5. # 客户端定义的时候需要写的代码
    ```python
    app = celery()

    #定义任务
    @app.task
    def send_sms():
        .....

    #然后发布任务
    send_sms.delay()
    ```
    1. 然后任务处理者,需要有完整的,和客户端一样的代码
    2. ## 所以,客户端的具体需要实现的函数,里面可以是pass,但是任务处理者里面一定是功能完整的代码
6. 开启celery worker
    1. 执行代码`celery -A 定义任务的python模块 worker -l info`
7. # 还是关于客户端的这边,需要改装一下,把真正想做异步处理的具体函数,比如是这个短信,下面这段代码是改造前的
    ```python
    # 发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
    ```
    改造后
    ```python
    #引用到celery导入进来的send_sms.delay()
    send_sms.delay()
    ```
8. ## 然后celery这端的任务者,继承上面的发送任务
    ```python
    @celery_app.tasks
    def send_sms(to, datas, temp_id):
        ccp = CCP()
        cpp.send_template_sms(to, datas, temp_id)
    ```
9. ## 关于返回值
    1. ## 不存在,直接告诉用于已经成功了.如果用户收不到短信的话,就直接甩锅吧!

10. ## celery的目录结构使用
    1. 如果异步任务比较多,就用目录的方式去管理
    2. 定义启动文件(main.py)
    3. 然后新建一个sms目录,专门用于管理发送短信的
        1. 关于配置文件,可以让参数单独写成一个配置文件.
    4. ### 然后可以引入配置信息
    ```python
    from celery import Celery
    from ihome.tasks import config
    celery_app = Celery("ihome")
    #引入配置信息
    #这个地方,可以引入对象作为配置信息,也可以导入模块,当作配置信息
    cerery_app.config_from_object(config)
    ```
    5. 然后在main文件,添加celery_app.autodiscover_tasks(["ihome.tasks.sms"])
11. 就是,在web中,多使用异步的这种东东.!
12. ## celery独立的目录使用
    1. 假如需要独立的话,仅仅只是依赖云通讯的那几个模块!.

13. ## celery接收返回值
    1. ## 不仅可以用目录的方式定义celery,还可以用工程的方式去定义
    2. 可以将main.py改名为celery.py,cerlery就会自动找到这个主文件了.
    3. 如果有返回值,直接返回
        ```python
        result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
        ```
    4. ### 通过get方法获取cerlery异步执行的结果
        ```python
        #get方法默认是阻塞的行为,会等到有了执行结果之后才返回
        #get方法也接受参数timeout,超时时间,超过超时时间还拿不到结果,就返回
        ret = result.get()
        ```
14. ## 结束