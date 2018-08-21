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

    file = request.file

    ```