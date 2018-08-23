# 房屋管理
1. ## 查询当前数据库的house信息
    1. 通过`houses = House.query.filter_by(id=user_id)`
    2. ### 通过查询user信息,`user = User.query.get(user_id)`
        1. 因为user有一个字段house是一对多的关系,所以也可以通过user查询到他对应的房子信息
        2. 然后就可以获取得到房源信息了`houses = user.houses`
    3. 然后在House模型类里面,专门设置了一个将对象转换成为字典的方法,将基本信息转换为字典数据
        ```python
        def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        house_dict = {
            "house_id": self.id,
            "title": self.title,
            "price": self.price,
            "area_name": self.area.name,
            "img_url": constants.QINIU_URL_DOMAIN + self.index_image_url if self.index_image_url else "",
            "room_count": self.room_count,
            "order_count": self.order_count,
            "address": self.address,
            "user_avatar": constants.QINIU_URL_DOMAIN + self.user.avatar_url if self.user.avatar_url else "",
            "ctime": self.create_time.strftime("%Y-%m-%d")
        }
        return house_dict
        ```
2. ## 主页就不用添加装饰器了
    1. 查询热门的数据就可以了.!
    2. 相关的属性,可以看一下config
    3. ### 有一个细节
        1. 如果这个房源信息,没有设置主页的图片
            1. 然后就直接用continue跳过
    4. 引入缓存.
        1. 一旦查询出结果,存到redis当中
        2. 也可以存json格式的数据!
    5. ### 向前端返回 涉及效率问题
        1. 问题1,现在可以直接向前端返回数组,但是jsonify里面是转换python的对象,例如是列表,字典之类的.
        2. 然后,尽量不要转换之后继续用jsonify再转换,因为这些转换都是很耗时.例如是,`return jsonify(errr=xxx,data=json_data)`,
            如果json_data已经是转换好的json数据的话,这一步的转换就有点浪费力气了.
        3. 解决
            1. `'{"error":"0","errmsg":"OK","data":$s}'%s
        4. #### 然后记得,补充状态码(200),和返回数据的类型(Content-Type:"application/json")))
    6. 数据到底是用缓存还是不不用?
        1. 注意好,使用try except,如果查询不到数据的话,出现异常,如果不使用else的话,就需要在出现异常后面紧接设置ret为空.!
    
    7. ### 房屋的详细信息数据
        1. 如果判断,让如果当前用户是房东自己,然后不能让房东自己提交订房按钮.
        2. 判断userid和houseid是否为同一个.
            1. 自行决定要不要返回显示数据
        3. 封装返回数据的方法
            1. 因为涉及的数据太多了.!
        4. 关于backref,也就是反向引用.这是一个relationship
        5. 补充backref,db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性,从而定义反向关
            系。这一属性可替代 role_id 访问 Role 模型,此时获取的是模型对象,而不是外键的值。
            1. 图 5-1 中的一对多关系在模型类中的表示方法如示例 5-3 所示。
            ```python
                示例 5-3
                hello.py:关系
                class Role(db.Model):
                # ...
                users = db.relationship('User', backref='role')
                class User(db.Model):
                # ...
                role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
                如图 5-1 所示,关系使用 users 表中的外键连接了两行。添加到 User 模型中的 role_id 列
                被定义为外键,就是这个外键建立起了关系。传给 db.ForeignKey() 的参数 'roles.id' 表
                明,这列的值是 roles 表中行的 id 值
            ```
            2. #### 部分名词
           
            |英文|中文|
            |----|--------------|
            |backref |在关系的另一个模型中添加反向引用|
            |primaryjoin |明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定|
            |lazy |指定如何加载相关记录。可选值有 select (首次访问时按需加载)、 immediate (源对象加载后就加载)、 joined (加载记录,但使用联结)、 subquery (立即加载,但使用子查询),noload (永不加载)和 dynamic (不加载记录,但提供加载记录的查询)数据库  49(续)|
            |uselist |如果设为 Fales ,不使用列表,而使用标量值
            |order_by |指定关系中记录的排序方式
            |secondary |指定 多对多 关系中关系表的名字
            |secondaryjoin |SQLAlchemy 无法自行决定时,指定多对多关系中的二级联结条件|
            
3. 稍稍补充一下,Flask系列：数据库,一对多,多对多,关系,简书
    1. https://www.jianshu.com/p/0c88017f9b46
    2. 部分摘抄资料
    >User(用户表)
    ```python
        >>> from sqlalchemy import Column, Integer, String
        >>> class User(Base):
        ...     __tablename__ = 'users'
        ...
        ...     id = Column(Integer, primary_key=True)
        ...     name = Column(String)
        ...     fullname = Column(String)
        ...     password = Column(String)
        ...
        ...     def __repr__(self):
        ...        return "<User(name='%s', fullname='%s', password='%s')>" % ( self.name, self.fullname, self.password)

    ```
    >
    ```python
    >>> from sqlalchemy import ForeignKey
    >>> from sqlalchemy.orm import relationship, backref

    >>> class Address(Base):
    ...     __tablename__ = 'addresses'
    ...     id = Column(Integer, primary_key=True)
    ...     email_address = Column(String, nullable=False)
    ...     user_id = Column(Integer, ForeignKey('users.id'))
    ...
    ...     user = relationship("User", backref=backref('addresses', order_by=id))
    ...
    ...     def __repr__(self):
    ...         return "<Address(email_address='%s')>" % self.email_address
    ```
    #### 解释
    ```python
        上述类使用了ForeignKey函数,它是一个应用于Column的指令,表明这一列的值应该保存指定名称的远程列的值。
        这是关系数据库的一个核心特征,是“胶水”,将原本无关的表变为有丰富的重叠关系的集合。上面的ForeignKey表示，
        Addresses.user_id列的值应该等于users.id列中的值，即，users的主键。

        第二个函数,称为relationship(), 它告诉 ORM ,Address类本身应该使用属性Address.user链接到User类。
        relationship()使用两个表之间的外键关系来确定这个链接的性质，这个例子中，确定Address.user将要成为
        多对一中多的一侧。relationship()的参数中有一个称为backref()的relationship()的子函数，
        反向提供详细的信息, 即在users中添加User对应的Address对象的集合，保存在User.addresses中。
        多对一关系的反向始终是一对多的关系。一个完整的可用的relationship()配置目录在基本关系模式。

        两个互补关系, Address.user和User.addresses被称为一个双向关系，
        并且这是SQLAlchemy ORM的一个关键特性。
        小节Linking Relationships with Backref详细讨论了“Backref”特性。

        relationship()的参数中，关联的远程类可以通过字符串指定,如果声明系统在使用。
        在上面的例子的User类中，一旦所有映射完成,这些字符串被认为是用于产生实际参数的 Python 表达式。
        允许的名字在这个评估包括,除其他方面外,所有类的名称已被创建的声明的基础。

    ```
# SQLAlchemy ORM教程之三：Relationship
https://www.jianshu.com/p/9771b0a3e589
# Basic Relationship Patterns
http://docs.sqlalchemy.org/en/rel_1_0/orm/basic_relationships.html#relationship-patterns