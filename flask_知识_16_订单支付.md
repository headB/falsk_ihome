# 支付,创建钥匙
1. 详细的可以阅读: https://open.alipay.com/platform/home/html
2. 关于沙箱环境(开发模拟环境)
3. 然后设置到公钥和私钥的知识点(还好我都比较理解了.!)
4. 还有一些API的说明!>
5. 公共请求参数
    1. 有什么作用.
        1. app_id
        2. method
        3. ......
6. 首先安装python的一些插件.
    1. pip install python-alipay-sdk --upgrade
    2. 生成密钥文件
    ```python
        openssl
        OpenSSL> genrsa -out app_private_key.pem   2048  # 私钥
        OpenSSL> rsa -in app_private_key.pem -pubout -out app_public_key.pem # 导出公钥
        OpenSSL> exit
    ```

7. 然后就是把这两个放到单独的keys文件夹里面。
8. 支付宝的密钥交换解释
    1. Q：和支付宝交换公钥是什么意思？
    A：私钥由开发者自行保管，把对应公钥提供给支付宝。相应的，支付宝提供自己的公钥给开发者，这称为交换公钥。
    开发者使用开发者私钥对请求内容签名，支付宝收到请求后，会使用开发者公钥进行验签，验签通过证明信息来源可靠并且未篡改。
    支付宝发送给开发者的数据中，支付宝也会使用自己的私钥进行签名。商户收到后，使用支付宝公钥验签，验签通过证明是支付宝发送的消息，并且未篡改。
9. 顺带一些ssh的知识
    1. https://www.cnblogs.com/ailx10/p/7664040.html
        1. 部分截图信息，请查看有道云笔记本的--置顶笔记本
    2. 但是单方向还是需要注意中间人攻击。
10. 

