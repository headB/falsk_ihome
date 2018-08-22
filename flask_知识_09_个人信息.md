# 图片存储服务的引入

1. # 问题
    1. 图片保存到本地,扩容(磁盘满的问题)
    2. 备份的问题
    3. 多机存储问题
    4. 重复图片问题
        1. 包括重名不同文件
        2. 不同文件名但文件内容相同.
    5. 解决方案
        1. FastDFS 快速分布式文件存储系统
        2. HDFS Hadoop hadoop分布式文件系统
        3. 七牛云存储
2. # 使用七牛
    1. `pip install qiniu`
    2. ## 使用七牛的put_data
        1. 为什么不用put_file
            1. 因为put_file还得指定一个文件名,所以这里就直接使用put_data就好了.!
    3. 使用put_data的时候,key就设置为None就可以了.!
    4. 简单的上传
    ```python
    with open("xx.jpg",'rb') as f:
        file_data = f.read()
        storage(file_data)
    ```
3. 获取文件 `f = request.files.get() `

# 上传用户图像
1. 在api下写profile.py
2. 添加好蓝图路径
3. 应用上一节的,如果要装饰函数的话,就多使用一个函数,返回被装饰函数的属性.
    ```python
    @api.route("xxx",methods=["POST"])
    @login_required
    def set_user_avatar():
        xxx
    ```
4.  部分代码
    ```python

    file1 = request.files.get()
    file1.read()

    ```
    1. 对对对,单一文件或者进入文件,最好还是设置一下,主文件启动,
    ```python
    if __name__ == "__main__":
        #这种形式
    ```
    2. 然后假如图片成功上传了,就得返回数据了,给flask的数据库记录图片的网址.
    3. 然后调用七牛图片.
        1. 使用try来捕获异常.
    4. 对用户对应的id模型类数据库更新头像的图片网址.
    5. ## flask对数据库进行更新操作
        1. User.query.filter_by(id=xx).update({"avatar_url":filename})
        2. session.commit()
        3. 如果有问题就session.rollback()
        4. 如果出问题可以记录一下日志

# 图片表单说明

1. ## 只要是传多媒体文件,你都要在form标签里面写`enctype="multipart/form-data"`
2. 然后input文件的type指明是"file",然后accept="image/*",作用是让用户筛选文件,
3. 既不想用ajax来处理上传图片的问题,但是普通的浏览器又不能处理
    1. 这个时候就引入一个插件!
        1. 引入`jquery.form.min.js`
        2. ### 还有一个问题,ajax里面的data这个数据,我们无法很方便地定义.
    2. 不知道为什么,每次绑定表单事件,都会回传一个参数回来,接收这个变量,随便起个什么名字都是可以的.!
        `e.preventDeafault`
    3. 调用插件的ajaxSubmit
        ```python
        $(this).ajaxSubmit({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
        ```
        1. 在另外一端如何接收提交过来的图片呢?
            1. 后端通过request.files.get("xx")获得的
    4. ### 重点难点
        1. 当上传的需求要求可预览、显示上传进度、中断上传过程、大文件分片上传等等，这时传统的表单上传很难实现这些功能，我们可以借助现有插件完成。
    5. ajaxSubmit
        1. jQuery使用ajaxSubmit()提交表单示例（转）
            https://blog.csdn.net/xinghuo0007/article/details/72806717
            1. jquery.form.js的ajaxSubmit和ajaxForm使用
                https://www.cnblogs.com/popzhou/p/4338040.html
    7. 如百度上传插件Web Uploader、jQuery图片预览插件imgPreview 、拖拽上传与图像预览插件Dropzone.js等等，大家可根据项目实际需求选择适合的插件。 
    8. ### 看一下flask如何保存图片
        1. 就是直接使用update更新数据的!.

