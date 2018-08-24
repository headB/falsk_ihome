# 表与表之间的关系
```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))

```
1. ## 上面两个表存在一定的关系
    1. 与django有一定区别的
    2. ### flask跟底层是靠近的.
    3. ### `parent_id`是真实存在在`Child`中的,所以得写数据类型的,在`django`那边是不用定义的.
    4. ### 但是仅仅用上面的步骤,是没有产生关联的,`ForeignKey('parent.id')`
        1. #### 注意了,ForeignKey后面的是表名+字段,注意了,是数据表
    5. relationship并不在数据库中的,所以这仅仅是描述关系,方便查询的.
        1. 当你操作`Parent`里面的children是关联那个对象呢,后面你就可以自己填写了,注意了,模型类考虑的.
    6. 以上的操作,已经可以让Parent查询到他下面都有那些Child信息了.

2. ## 但是,加入Child需要展示信息,上面的id可以方便展示,但是`parent_id`只是一个普通的Integer属性,只能显示数字
    1. 所以,得在上面的`Parent`,里面的children的relationship,添加其他属性,添加`backref="parent"`

3. 除了使用模型类的名字去查询数据库数据query，还有一种语法就是，写db.session.query(Role).all(),其中db意思是指db = SQLAlchemy(app)这个db.

4. ## filter是万能查询。
    1. ### 注意了，`filter（User.name=="xx").first()`,字段必须是这种，直接引用模型类的。然后`==`代表的是，一个普通的`=`
        2. 多条记录`filter（User.name=="xx"，User.id=='yy').all()`
    2. ### 还可以引入 或者  `from sqlalchemy import or_
        1. 例子`User.query.filter(or_(User.name=='wang',User.email.endswith("163.com"))`
    3. ### offset ,意思是从第几条开始取数据，limit是限制
        1. example：`User.query.filter（User.name=="xx").offset(2).all()`，意思是跳过前两条。
    4. ### 注意了，limit是限制，但是后面必须取数据，意思是，`User.query.filter（User.name=="xx").offset(2).limit(2).all()`这种形式
    5. 排序 order_by(),但是不是很通用
        1. example: `User.query.order_by("-id").all()`
        2. 这个才是推荐使用的方法，`User.query.order_by(User.id.desc()).all()`
    6. group_by分组
        1. `select name,id,count(id) from xxx group_by id`
        2. 导入`from sqlalchemy import func`
            1. 示例`db.session.query(User.role_id,funct.count(user.role_id)).group_by(user.role_id).all()`
    7. 