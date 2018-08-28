# 关于flask中，csrf过期的优化
1. 因为获取csrf的数值也是依赖浏览器中给定的session的数值。
2. ## 优化
    1. 所以，在配置项中，添加Session(app),把数据存到redis当中。这个是利用`flask-session`
    2. 因为请求过程是
        1. 首先去前端的cookie取一个值
        2. 然后到请求体或者python中
        3. 然后就进行校验
        4. ### flask-session是flask框架的session组件，由于原来flask内置session使用签名cookie保存，该组件则将支持session保存到多个地方
    3. 解决：
        1. 引入flask-session机制的话，默认的这些数值就不存在前端的cookie里面了。
        2. 然后提取`csrf_token`的数值的话，现在就从redis里面提取了。
            1. `csrf_token = redis.get('redis')`
        3. flask-session在进行的时候，就添加了一个钩子（感觉很装饰器），对所有内容进行验证。
    4. ### 想起来了一个很重要的问题，就是，原来之前的csrf的对比值，是对比session里面的csrf和body发送过来的csrf的数值进行对比。
        1. 现在优化的这部分，是body对比redis中的数值。
    5. ### 有三个地方存在csrf数值。
3. ## 重点了，如果如何呢？
    1. 在退出的时候，不一次性删除
        1. 首先提取csrf并且保存
        2. 然后再使用session.clear
        3. 然后就设置回去
4. 为什么放到最后才讲？
    1. 为了就是认识csrf的认证机制。

# 关于数据库优化介绍
1. ## 如何解决并发问题
    1. 最重要就是解决数据库的问题了。
    2. 具体的优化细项目，请看目录里面的note.txt
    3. 表结构设计
        1. 扩展
        2. 查询的快慢问题
        3. 三范式 https://www.zhihu.com/question/24696366
            1. 表要拆到不能再猜
            2. 只保留主要的，非主要就提取出来
            3. 非主要表，继续来拆分表
                1. 如果某一部分的数据丢失的话，不至于影响全部的数据。
    4. ## 查询优化->建立索引 菜鸟的讲解 http://www.runoob.com/mysql/mysql-index.html
        1. 比如说现在`select * from ih_house_info where id=1;`
        2. ### 实际上，上面的这些操作，是不断地去数据库逐条数据查询的，这样想当浪费时间。
        3. 如何快速查询
            1. 建立索引。（酒店前台，小姐姐围护的那个表，就是索引了，公安通过问小姐姐，直接就可以定位具体的数据在哪里，这就是索引了。）
        4. ### 再次说明，其实，主键也是属于主键的一种，所以，查询`id`的时候，其实想当于可以直接找小姐姐拿数据了。
        5. ### 还有唯一约束
            1. 建立约束的时候也就是同时建立了主键
        6. ### 索引 （key，index)
            1. 在sql语句中
            2. 通过`show create table xx`可以查询表结构
                1. 顺便可以查询索引有那些
            3. ### 联合主键，联合索引
                1. 如果经常查询重复出现两个主键，那就整合两个主键为联合主键
                2. #### SQL的实现方式:key `a_b_key` (a,b)
                3. 不是直接放`index=True`,在flask里面实现： db.index("a_b",a,b)
                4. #### 关于联合索引修改的问题 http://www.jianshu.com/p/2b541c028157
                    1. `alter table mytable add index name_city_age (name(10),city,age)`
                        1. ##### 对应上面的问题，建表时，username长度为16，这里用10，因为一般情况下名字和长度不会超过10
                        这样可以加速索引查询速度，还会减少索引文件的大小，提高INSERT的更新速度。
                    2. 然后查询的时候，必须是`username,city,age`或者`username,city`或者`username`，如果
                    都不是上面的这些形式的话，索引就白建立了。
        7. ### 但是还是有坏处
            1. 降低增删改的速度
            2. 所以说，也不能设置过多
        8. 通过index创建索引
            1. `create INDEX indexName ON mytable(username(length))
            2. 代码
            ```python
            CREATE TABLE mytable(
                ID INT NOT NULL,
                username VARCHAR(16) NOT NULL,
                INDEX [indexName] username(length))
            );
            ```
            3. 删除的方法
            `drop INDEX [indexName] ON mytable`
    5. ### 最左原则。
        1. 就是关于查询的时候，建议where后面的条件顺序，最后把有建立索引的字段放在最前面
    6. ### 修改表索引
        1. 
    7. ### 关于django的优化小提及
        1. 如果模型类查询速度实在太慢了，就手动查询语句
            1. 只要在程序中去查询的话，一定不要使用`select *`,效率不一定高，主要是没有必要，尽量就节约网络流量。
    8. ### 可以使用联合查询，就尽量不适用嵌套查询（子查询）
        1. `join`是联合查询
        2. `select xx from xx where filed = (select xx from yy )`是子查询
2. ## 外键，作用，保证数据的完整性。
    1. 如果使用参数选项，`cascade`级联，就可以删除外键的时候，顺便删除对应牵连的数据（围护外键有额外开销，影响性能）
    2. 使用分析工具分析效率低的sql语句   慢查询工具
        https://flyerboy.github.io/2016/12/23/mysql_slow/
        https://yemengying.com/2016/05/24/mysql-tuning/
    3. ### 如果数据大的时候，不在使用外键
3. ## 缓存
    1. redis
    2. memcached
4. 读写备份
    1. 读写分离
    2. 主从备份
    2. 主从热备份
        1. 查的操作可以和增删改分离。
5. ## 分库分表（上亿，几千万的数据）
    1. http://www.infoq.com/cn/articles/key-steps-and-likely-problems-of-split-table
    2. ### 垂直分表（通俗的说法是，"大表拆小表")
        1. 某一个表中的字段过多，就可以新建立一张扩展表
    3. ### 垂直分库
        1. 以数据库的方向来切。
        2. 比如说，订单就单独分为一个数据库，用户就分为一个单独的数据
    4. ### 水平分表（用得最多）
        1. 相同的字段，不过分几个表来保存这些类似的数据，例如xx_user1,xx_user2
        2. 但是预防id重复，主键重复。
            1. 自己维护id表
            2. 而且这个分表了，但是，还是在同一个磁盘操作，所以还是会卡的。
            3. 把数据表都设置在不同的数据库，不同的主机当中。

# 工作流程
1. 分析需求
2. 编写代码
3. 编写单元测试
4. 自测
5. 编写接口文档
6. 提测代码

# 账号
1. email
2. git账号（gitlab)
    1. 权限
        1. 具体产品
    2. rsa密钥
3. vpn账号 阿里云，腾讯云，aws亚马逊
4. 公司可能让你去熟悉公司的业务，代码等等。
5. 
        