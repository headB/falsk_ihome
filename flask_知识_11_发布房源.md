# 保存房屋基本信息数据后端编写
1. 整理好前端的基本信息
2. 还有配套设施(有冇WIFI/空调/暖气等等))
3. 补充一下check,`<li class="col01"><input type="checkbox" name="sku_ids" value={{ sku.id }} checked></li>`
4. checkbox,不做特殊处理,只返回name和true值
    1. 首先需要传递id数值
        1. 理想传递是这样的`"facility":['7','8']
    2. 如何传递id数值
        1. 
5. ## 后端接收数据
    1. house_data = request.get_json()
    2. xx = house_data.get('xx')
    3. 然后就检验参数
        1. 如果参数有问题,可以引起异常
    4. 业务处理
        1. 保存数据
        ```python
        house = House(user_id=user_id,area_id=area_id,title=title,address=address,room_count=room_count,acreage=acreage,xxx)
        try:
            db.session.add(house)
            #db.session.commit()
        except Exception as e:
            db.session.rollback()
        ```
        2. ### 准备处理房屋的设施信息
            1. 代码
            ```python
            #如果用户勾选了再保存数据库信息

            #需要进行过滤
            facxxx_ids = house.get('')
            if facilities:
                try:
                    Facility.query.filter(Facility.id.in_(facxxx_ids))
                except Exception as e:
                    return jsonify("xxx")
            
            if facilities:
                #表示有合法的数据
                #保存设施数据
                #利用关联数据库保存数据
                house.facilities = facilities
                try:
                    db.session.add(house)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    retutn "xxx"
            ```
        3. ### 需要过滤信息表
        4. 看了一下,Facility这个数据库模型类,居然只有id和name信息.
        5. return house_id
6. ## 上传图片是需要house_id的.

# 保存房屋图片后端编写
1. 两个装饰器`@api.route+@login_required`
2. 请求house_id
```python
iamge_file = request.files.get("house_image")
house_file = request.form.get("house_id")
```
3. 判断house是否存在
    1. 使用try
4. 调用函数去保存图片到七牛服务器.!
```python
try:
    file_name = storage(image_data)
except Exception as e:
    current_app.logger.error(e)
    return jsonify()
```
5. 然后就保存数据,flask,多个数据库同时保存信息.
```python
# 保存图片信息到数据库中
house_image = HouseImage(house_id=house_id, url=file_name)
db.session.add(house_image)

# 处理房屋的主图片
if not house.index_image_url:
    house.index_image_url = file_name
    db.session.add(house)

try:
    db.session.commit()
except Exception as e:
    current_app.logger.error(e)
    db.session.rollback()
    return jsonify(errno=RET.DBERR, errmsg="保存图片数据异常")

```
6. 然后拼接一下链接.!

# 补充一下关于db.session的知识.
1. 多个数据库插入数据库,可以一次db.session.add(xx)
    1. 如果先一次性写完,可以写成列表的形式,db.session.add_all([xx1,xx2])
2. flask更新数据
    1. db.session.add(xx)
    2. db.session.commit()
3. flask删除行
    1. db.session.delete(xxx)
    2. db.session.commit()

# 保存房屋基本信息前端代码
1. 什么是serializeArray()
    1. serialize()序列化表单元素为字符串，用于 Ajax 请求。
    2. serializeArray()序列化表单元素为JSON数据。
2. 获取前端数据`$("#form-house-info").serializeArray()`
3. js的map方法
    1. `$("#form-house-info").serializeArray().map(function(x){data['x.name']=x.value})`
    2. 然后直接查看data数据就知道数据已经组织好了.!
4. 但是,看图,有道云笔记的,标题和上面的对应.
    1. facxxxx需要特殊处理一下.!
        1. ```js 
            var facXX = []
            
            $(":checked[name=facility]").each(function(index,x){facXX[index] = $(x).val()})
            ```
            上面的说明:x是一个对象,所以还得用jq去再获取一下数值
    2. 补充js的each知识
        1. 参数	描述
        function(index,element)	
        必需。为每个匹配元素规定运行的函数。

        index - 选择器的 index 位置
        element - 当前的元素（也可使用 "this" 选择器）
5. 然后整理好数据之后,就往后端塞数据了.!
    ```python
        $.ajax({
            url: "/api/v1.0/houses/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
    ```

# 发布房源
1. 前端
    1. 表单的提交
        1. 引入异步提交的js插件,form.js
    2. data参数就不用管,等插件自己处理就可以了.
2. 然后成功的回调函数,里面对`$(".house-image-cons").append('<img src="xxxx">')`