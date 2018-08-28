# 关于flask中，csrf过期的优化
1. 因为获取csrf的数值也是依赖浏览器中给定的session的数值。
2. ## 优化
    1. 所以，在配置项中，添加Session(app),把数据存到redis当中。这个是利用`flask-session`
    2. 