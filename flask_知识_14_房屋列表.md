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

2. ## 然后就是排序
    1. 按照传递过来的参数

# 房屋列表页分页补充与测试
1. page的使用(前期准备)
    1. 在flask中使用分页更加的方便，直接在查询结果后面添加就可以了
        1. example:`paginate = User.query.order_by("-id").paginate()`
    2. 处理分页
        1. page_data = paginate.items
        2. 代码
        ```python
        page_obj = User.query.order_by("-id").paginate(page=page,per_page=x,error_out=False)
        ```
    3. 获取页面数据`house_li = page_obj.items`
        1. 转换成为字典的形式
            1. 代码
            ```python
            house_li = page_obj.items
            houses = []
            for house in house_li:
                houses.append(house.to_base_dict()) ## 恩恩，to_base_dict是定义在models里面的
            
            #同时返回总页数
            total_page = page_obj.pages

            return jsonify("xxx")
            ```
# 解析_等好参数，也就是，我不理解的条件查询
1. `House.area_id == area_id`这个，filter，条件表达式，实质他是一个`BinaryExpression object`
2. 所以，这不是普通的用法
3.  `House.area_id == area_id` 等价于 `House.area_id.__eq__(1)`

# 房屋列表页缓存处理
1. 

# redis的pipeline的使用
1. ## 重要
    1. 恩恩。很类似linux的shell的管道命令，就是，一次性可以执行多个操作
    2. 使用，代码
    ```python
    #创建管道对象，可以一次性执行多个语句
    pipeline = redis_store.pipeline()
    #开启多个语句的记录
    pipeline.multi()

    pipeline.hset(redis_key,page,resp_json)
    pipeline.expire(redis_key,xxx)

    #然后执行
    pipeline.execute()

    ```

# 前端编写
1. 随着滚动，不断加载数据
    1. 在前端会设置页数，当前页，总页数，
    2. 填充页面
        1. 请求了新的页面数据，形式是追加
        2. 还有一种
            1. 如果改变了条件，就重新填充了。
2. 部分代码
    1. 代码-解析url中的查询字符串
    ```js
    function decodeQuery(){
        var search = decodeURI(document.location.search);
        return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
            values = item.split('=');
            result[values[0]] = values[1];
            return result;
        }, {});
    }
    ```
3. # `2018年8月26日补充`
    1. 页面加载好了,就提取url的参数,去获取后台数据
    2. ## 稍微详细一点点说明上面的流程
        1. 首先,flask根据前端传送过来的请求,加载search.html,这个页面都是纯的html+css+js,此时并没有向后台查询数据
        2. 然后当加载到js部分的时候,就进行了一系列的操作
            1. 首选是根据当前页面的url参数,整理了一下
            2. 然后这个时候才正式向后端查询当前的房屋情况.get请求.
    3. ## 改变当前的搜索条件
        1. ### 如果重新点击时间,位置和指定选项,如何做出改变呢
        2. 答案就是
            1. #### 前端写了一个空白区域的监听,$("display-mask")
            2. 当这个区域被选中,被点击,就意味着需要重新搜索了.


    2. 部分介绍
    
        语法
        array.reduce(function(total, currentValue, currentIndex, arr), initialValue)
        参数
        参数 	描述
        function(total,currentValue, index,arr)	必需。用于执行每个数组元素的函数。
        函数参数:
        
        |参数 |	描述|
        |-----|------|
        |total	|必需。初始值, 或者计算结束后的返回值。|
        |currentValue |	必需。当前元素|
        |currentIndex	|可选。当前元素的索引|
        |arr	|可选。当前元素所属的数组对象。|
        initialValue	|可选。传递给函数的初始值|
    
    2. ## 当文档加载好了以后的工作流程
    ```js
    $(document).ready(function(){
    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);

    ```
    3. js如何获取当前url地址信息,如何获取url地址参数
        1. document.location."当前页后缀",例如`document.location.search`
    4. decodeURL
        1. decodeURI() 函数可对 encodeURI() 函数编码过的 URI 进行解码。
            1. 实例
            ```python
            #在本例中，我们将使用 decodeURI() 对一个编码后的 URI 进行解码：
            <script type="text/javascript">
            var test1="http://www.w3school.com.cn/My first/"
            document.write(encodeURI(test1)+ "<br />")
            document.write(decodeURI(test1))
            </script>
            #输出：
            http://www.w3school.com.cn/My%20first/
            http://www.w3school.com.cn/My first/
            ```
        2. decodeURI与decodeURIComponent区别
            https://www.cnblogs.com/hamsterPP/p/7131163.html

        3. js的reduce用法
            1. reduce() 方法接收一个函数作为累加器，数组中的每个值（从左到右）开始缩减，最终计算为一个值。
            2. 实例
            ```js
            var numbers = [65, 44, 12, 4];
            function getSum(total, num) {
                return total + num;
            }
            function myFunction(item) {
                document.getElementById("demo").innerHTML = numbers.reduce(getSum);
            }
            #结果125
            ```
    5. ## 后续
        1. each的用法
        ```js
        var arr = [ "one", "two", "three", "four"];
        $.each(arr, function(){
            alert(this);
        });
        ```
    6. 1