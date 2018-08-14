# 这里是视图吗?

from . import api


@api.route("/index")
def index():
    return "index page"