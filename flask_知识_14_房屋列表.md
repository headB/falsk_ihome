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
