# 房屋列表业务分析

1. 根据条件进行搜索,得出结果
    1. 条件:入住时间,位置区域,最新上线
    2. 但是默认不是上面的三个条件,而是一个默认的排列结果
    3. 区域信息和价格都好处理
    4. ## 重点是处理时间
        1. 问题是,House模型类里面,并没有专门记录时间的字段
        2. 关于时间问题,现在关联到订单信息这边来了
        3. ### 时间筛选方便,去查询这段时间里面,订单有没有相应的记录,如果就,就排除这个房源信息

# 房屋列表后端参数判断
1. 获取房屋的列表信息
2. ## 时间处理
    1. 获取get过来的参数,然后`start_date = request.args.get("sd","")`,后面的为空,意思就是如果参数为空的话,就设置默认为空.
        1. 结束时间和上面类似了.
    2. 其他的非时间参数,也是如果没有获取到参数,就默认设置为空.
3. ## 时间转换
    1. 然后利用datetime将字符串的日期转换为python的时间对象
        1. `datetime.strptime(start_date,"%Y-%m-%d")`
        2. ### 因为前端传递过来的格式不一定每次都是正确的,所以,必须,使用try来排除异常
    2. 补充生成现在时间的方法,datetime
        1. 代码
        ```python
        datetime.datetime.now()
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ```
    3. ### 一言不合就使用断言,`assert start_date <= end_date`
4. 判断区域id
    1.  代码
    ```python
    try:
        area = Area.query.get(area_id)
    except Exception as e:
        #记录日志
        current_app.logger.error(e)
        return jsonify("xxx")
    ```
5. 处理页数
    1. 和上面的判断区域id差不多的步骤
    2. 尝试将获取到的p,用int去转换
        1. 如果转换失败,就是使用异常处理去设置为默认

# 构造时间条件

1. ## 查询数据库
    1. ### 这个位置可以对参数进行拆分,因为这个位置要接收很多的参数进行数据库查询
        1. 例如,时间,区域,等等信息
        2. 填充过滤参数,参数不确定
            1. 代码，留意好filter_params，filter的用法。
            ```python
            filter_params = []

            #填充过滤参数

            ```
        3. #### 比较难搞时间交叉的时间
            1. 查询冲突的房子`select * from order where order.begin_data<=end_date and order.end_date >= start_date`
            2. #### 我用边界的思想去想象，就是，区域如果是重叠的话，达到边界就触发
            3. 彼此的边界还是有接触的话，就证明还是存在交集的，恩恩，就是这样了。！
            4. not in,notin查询，还有条件的组装，多重条件的组装查询，区域，时间，
                1. 代码
                ```python
                if conflict_orders:
                    # 从订单中获取冲突的房屋id
                    conflict_house_ids = [order.house_id for order in conflict_orders]

                    # 如果冲突的房屋id不为空，向查询参数中添加条件
                    if conflict_house_ids:
                        filter_params.append(House.id.notin_(conflict_house_ids))

                # 区域条件
                if area_id:
                    filter_params.append(House.area_id == area_id)

                # 查询数据库
                # 补充排序条件
                if sort_key == "booking":  # 入住最多
                    house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
                elif sort_key == "price-inc":
                    house_query = House.query.filter(*filter_params).order_by(House.price.asc())
                elif sort_key == "price-des":
                    house_query = House.query.filter(*filter_params).order_by(House.price.desc())
                else:  # 新旧
                    house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())
                ```
            
        2. House.query.filter()
        3. #### 关于filter的用法，语法，filter比起filter_by更加强大，支持比较运算符，支持or_、in_等语法。
            1. https://www.cnblogs.com/Orangeorchard/p/8133795.html
            2. https://blog.csdn.net/bieguolaia/article/details/77922605
                1. 部分代码
                ```python
                # 查询 id 等于 1 的数据，只显示第一条。多个条件也是可以的。但格式只能是 key=value 的方式，多条件关系为 and。
                print(User.query.filter(User.id == 1).first())
                print(User.query.filter(User.id == 1, User.name == "小王").first())
                # 先注意一下 filter 与 filter_by 参数写法上的区别。
                # 另外再注意一下：filter 是 不 支 持 x and x 或者 x or x 这样的操作的，虽然这样写不报错...
                # filter 支持的操作是 > < = != 这些，当然还有上面 filter_by 的那种关系 x, y -> x and y。
                # 那要用这种 and、or 怎么办 ？
                from sqlalchemy import and_, or_
                print(User.query.filter(and_(User.id == 1, User.address == "BJ")).first())
                print(User.query.filter(or_(User.id == 1, User.address == "SH")).first())
                # 对，就这么搞
                print(User.query.filter_by(id=1).value("name"))
                print(list(User.query.filter_by(id=2).values("name", "address")))
                # 输出匹配数据的指定字段，默认是 select * form xxx，现在是 select name, address from xxx。
                # 又要注意了：.value 只能用于找到的对象是一个时，例如找到多个对象，则 .value 只返回第一个对象的值。
                ```
            3. 提及一下django的知识点先，就是，在django里面，使用filter添加多个查询条件，他们的关系是`and`关系，
                1. 使用Q对象进行复杂查找
                    1. 关键字参数查询 - 输入filter()等 - 是“AND”编辑在一起。如果需要执行更复杂的查询（例如，带OR语句的查询），则可以使用。Q objects
            4. flask数据库里面的filter_by用法，House.query.filter_by(user_id=user_id)，这个就是才用关键字了。Models模块里面的House模型类的确存在一个user_id这个字段
            5. 

2. ## 