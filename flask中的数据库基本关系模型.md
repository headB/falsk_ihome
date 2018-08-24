基本关系模式
快速了解基本关系模式。

用于以下每个部分的导入如下：
```python
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```
一对多

一对多关系将外键放在引用父对象的子表上。 relationship()然后在父项上指定，作为引用子项表示的项集合：

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
要在一对多中建立双向关系，其中“反向”是多对一，请指定一个附加relationship()并使用以下relationship.back_populates参数连接两者：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="children")

```
Child将获得parent具有多对一语义的属性。

或者，该backref选项可用于单个relationship()而不是使用 back_populates：
重点！这个backref,原来只是一个名字而已！
![image.png](https://upload-images.jianshu.io/upload_images/4151356-03874685b6eb8b10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", backref="parent")
```
------
多对一
多对一将外键放在引用该子对象的父表中。 relationship()在父级上声明，将创建一个新的标量持有属性：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
通过添加秒relationship() 并relationship.back_populates在两个方向上应用参数来实现双向行为：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", back_populates="parents")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parents = relationship("Parent", back_populates="child")
或者，backref参数可以应用于单个relationship()，例如Parent.child：

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref="parents")
```

------
一对一
One To One本质上是双向关系，双方都有标量属性。为实现此目的，该uselist标志指示在关系的“多”侧放置标量属性而不是集合。将一对多转换为一对一：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child = relationship("Child", uselist=False, back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="child")

```
或多对一：

```python
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent = relationship("Parent", back_populates="child", uselist=False)

```
与往常一样，可以使用relationship.backref和backref()函数来代替relationship.back_populates方法; 要uselist在backref 上指定，请使用以下backref()函数：


```python
from sqlalchemy.orm import backref

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref=backref("parent", uselist=False))

```
------
多对多
Many to Many在两个类之间添加了一个关联表。关联表由secondary参数表示 relationship()。通常，Table使用MetaData 与声明性基类关联的对象，以便ForeignKey 指令可以找到要链接的远程表：
```python
association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary=association_table)

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)

```
对于双向关系，关系的两侧都包含一个集合。指定using relationship.back_populates，并为每个relationship()指定公共关联表：

```python
association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship(
        "Child",
        secondary=association_table,
        back_populates="parents")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    parents = relationship(
        "Parent",
        secondary=association_table,
        back_populates="children")

```
当使用backref参数代替时 relationship.back_populates，backref将自动使用相同的secondary参数作为反向关系：

```python
association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary=association_table,
                    backref="parents")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
所述secondary的论点relationship()也接受返回最终的说法，当第一次使用映射器，其仅被评估一个可调用。使用它，我们可以association_table在以后定义，只要在所有模块初始化完成后它可用于callable：

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary=lambda: association_table,
                    backref="parents")
使用声明性扩展时，也接受传统的“表的字符串名称”，匹配存储在Base.metadata.tables以下表中的表的名称：

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary="association",
                    backref="parents")


删除多个表中的行
这是唯一的一个行为secondary参数relationship() 是，Table它在这里指定为自动受INSERT和DELETE语句，如对象添加或从集合中删除。有没有必要从该表中手动删除。从集合中删除记录的行为将具有在flush上删除行的效果：
```python
# row will be deleted from the "secondary" table
# automatically
myparent.children.remove(somechild)
经常出现的一个问题是当子对象直接递送到“辅助”表中的行时如何删除Session.delete()：

session.delete(somechild)
```
这里有几种可能性：

如果存在relationship()from Parentto Child，但 没有将特定链接Child到每个的反向关系Parent，则SQLAlchemy将不会意识到在删除此特定 Child对象时，它需要维护将其链接到的“辅助”表Parent。不会删除“辅助”表。
如果存在将特定链接Child到每个特定的关系Parent，假设它被调用Child.parents，默认情况下SQLAlchemy将加载到Child.parents集合中以查找所有Parent对象，并从建立此链接的“辅助”表中删除每一行。请注意，此关系不需要是bidrectional; SQLAlchemy严格查看relationship()与Child被删除对象相关的每个内容。
这里性能更高的选项是使用ON DELETE CASCADE指令和数据库使用的外键。假设数据库支持此功能，则可以使数据库本身自动删除“辅助”表中的行，因为删除了“child”中的引用行。Child.parents 在这种情况下，可以指示SQLAlchemy 使用passive_deletes 指令on 来放弃在集合中的主动加载relationship(); 有关详细信息，请参阅使用被动删除。
请再次注意，这些行为仅与使用的secondary选项相关relationship()。如果处理显式映射且不存在于secondary相关选项中的关联表，则relationship()可以使用级联规则来自动删除实体以响应被删除的相关实体 - 有关此功能的信息，请参阅级联。

>关联对象

关联对象模式是多对多的变体：当关联表包含除左表和右表外键之外的其他列时，它会被使用。secondary您可以将新类直接映射到关联表，而不是使用参数。关系的左侧通过一对多引用关联对象，关联类通过多对一引用右侧。下面我们说明映射到的关联表Association，其包括称为柱类extra_data，它是与之间每个关联一起存储的字符串值Parent和 Child：

```python
class Association(Base):
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child")

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Association")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)

```
与往常一样，双向版本使用relationship.back_populates 或relationship.backref：


```
class Association(Base):
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")
```
以直接形式使用关联模式要求子对象在被附加到父对象之前与关联实例相关联; 类似地，从父级到子级的访问通过关联对象：

```python
# create parent, append a child via association
p = Parent()
a = Association(extra_data="some data")
a.child = Child()
p.children.append(a)

# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print(assoc.extra_data)
    print(assoc.child)

```