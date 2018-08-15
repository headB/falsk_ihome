# 图片单独一个表

1. 为什么需要单独建表
    1. 字段数量不确定性,比如说这里有3个iamges1,2,3字段,但是每一次不一定3个字段都使用.
    2. 尽量不调整表结构就不调整.!
2. 以空间换时间.
    1. 冗余字段.
    2. 

# 项目模型类型说明
1. ## 跟django一样,需要设置一个父类,里面设置好
    1. 更新时间
    2. 创建时间
    3. 但是有个问题,我没有看到他的BaseModel写明是父类,
    4. 代码
        ```python
        class BaseModel(object):
                """模型基类，为每个模型补充创建时间与更新时间"""

                create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
                update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

        class Area(BaseModel, db.Model):
                """城区"""

                __tablename__ = "ih_area_info"

                id = db.Column(db.Integer, primary_key=True)  # 区域编号
                name = db.Column(db.String(32), nullable=False)  # 区域名字
                houses = db.relationship("House", backref="area")  # 区域的房屋
        ```
    5. ## 多对多关系
        1. 代码
            ```python
                # 房屋设施表，建立房屋与设施的多对多关系
                house_facility = db.Table(
                    "ih_house_facility", ##第一个对应的是创建表的名字
                    ##
                    db.Column("house_id", db.Integer, db.ForeignKey("ih_house_info.id"), primary_key=True),  # 房屋编号
                    db.Column("facility_id", db.Integer, db.ForeignKey("ih_facility_info.id"), primary_key=True)  # 设施编号
                )
            ```
        2. ### 联合主键
            1. 把house_id和facility_id结合起来,组成联合主键.!
            2. 设置方法就是同时设置成为联合主键.!
        3. 图片参考,请参考2018年8月15日的有道云笔记截图
        4. ### 过滤关系,利用second关键起来!.
            1. 代码
                ```python
                    class House(BaseModel, db.Model):
                    """房屋信息"""

                    __tablename__ = "ih_house_info" 

                    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋的设施

                ```
    6. ## 补充多对多的知识点
        1. 多对多关系是关系数据库中两个表之间的一种关系， 该关系中第一个表中的一个行可以与第二个表中的一个或多个行相关。第二个表中的一个行也可以与第一个表中的一个或多个行相关。 [1] 
        2. 详细
            实例解释
            比如在常见的订单管理数据库当中“产品”表和“订单”表之间的关系。单个订单中可以包含多个产品。另一方面，一个产品可能出现在多个订单中。因此，对于“订单”表中的每条记录，都可能与“产品”表中的多条记录对应。此外，对于“产品”表中的每条记录，都可以与“订单”表中的多条记录对应。这种关系称为多对多关系，因为对于任何产品，都可以有多个订单，而对于任何订单，都可以包含许多产品。请注意，为了检测到表之间的现有多对多关系，务必考虑关系的双方。 [1] 
        3. ### 要表示多对多关系，您必须创建第三个表，该表通常称为联接表，
            它将多对多关系划分为两个一对多关系。将这两个表的主键都插入到第三个表中。因此，第三个表记录关系的每个匹配项或实例。例如，“订单”表和“产品”表有一种多对多的关系，这种关系是通过与“订单明细”表建立两个一对多关系来定义的。一个订单可以有多个产品，每个产品可以出现在多个订单中。
        4. ### mysql表的一对一/一对多/多对多联系
            https://www.cnblogs.com/panxuejun/p/5975753.html
    7. 数据库设计范式
        https://www.cnblogs.com/knowledgesea/p/3667395.html

    8. 模型类已经创建好了,现在进行数据库迁移.!
        1. 使用命令
            ```python
            #第一步
            python manage.py db init
            #第二步
            python manage.py db migrate -m 'init tables'
            #

            ```
        2. 如果显示nodatabase change,解决办法
            1. 在demo导入model.
        3. 升级,更新(相当于迁移,migrate)
            ```python
            python manage.py db upgrade
            ```
    