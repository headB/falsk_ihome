# 这里是视图吗?

from . import api


@api.route("/v1.0/index")
def index():
    return "index page"