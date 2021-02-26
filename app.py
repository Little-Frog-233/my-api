import sys
sys.path.append('./')
import json
from flask import Flask, session, request, Response, redirect, url_for, flash, render_template, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cache import Cache
from flask_restful import Api
from flask_docs import ApiDoc
from conf.config import Config

conf = Config()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

########################文档注册###############################
ApiDoc(app)

#######################启用缓存###############################
# 配置redis作为缓存
redis_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': conf.redis_cache,
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': '2',
    'CACHE_REDIS_PASSWORD': ''
}
cache = Cache(app, config=redis_config, with_jinja2_ext=False)


########################启用跨域###########################
@app.after_request
def cors(environ):
    origin = '*'
    environ.headers['Access-Control-Allow-Origin'] = origin
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers[
        'Access-Control-Allow-Methods'] = 'HEAD,OPTIONS,GET,POST,DELETE,PUT'
    environ.headers[
        'Access-Control-Allow-Headers'] = 'x-requested-with,content-type,accept-token,Accept-token,Content-Length,Authorization,Accept,X-CSRFToken,CSRFToken-Id'
    return environ


########################限制器###########################
limiter = Limiter(app=app,
                  key_func=get_remote_address,
                  default_limits=["5/minute"])


@limiter.request_filter
def filter_func():
    """
	定义一个限制器的过滤器函数,如果此函数返回True,
	则不会施加任何限制.一般用这个函数创建访问速度
	限制的白名单,可以使用某些celeb集中处理需要
	limiter.exempt的情况
	"""
    path_url = request.path
    forbidden_url = []
    if all([i not in path_url for i in forbidden_url]):
        return True
    else:
        return False


########################注册Restful Api###########################
from api.index import *

########################restful-中文###############################
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


########################初始页面##########################
@app.route('/')
def index():
    return 'welcome to my api'


if __name__ == '__main__':
    app.run()