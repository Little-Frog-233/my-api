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

########################配置sqlalchemy###############################
from utils.mysql.models import *
HOST = conf.sql_host
PORT = conf.sql_port
DATABASE = conf.sql_database
USERNAME = conf.sql_username
PASSWORD = conf.sql_password
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(
        username=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        db=DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

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


######################Origin验证###############################
@app.before_request
def checkOrigin():
    try:
        origin = request.headers.get("Origin", None)
        if origin is None:
            raise ("Origin can not be None")
    except:
        if not request.referrer:
            abort(404)
        origin = request.referrer.replace('http://',
                                          '').replace('https://',
                                                      '').split('/')[0]
    urls = ['127.0.0.1:8080']
    if not any([i in origin for i in urls]):
        abort(404)


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
                  default_limits=["60/minute"])


@limiter.request_filter
def filter_func():
    """
	定义一个限制器的过滤器函数,如果此函数返回True,
	则不会施加任何限制.一般用这个函数创建访问速度
	限制的白名单,可以使用某些celeb集中处理需要
	limiter.exempt的情况
	"""
    path_url = request.path
    forbidden_url = ['nlp/sentiment']
    if all([i not in path_url for i in forbidden_url]):
        return True
    else:
        return False


########################注册Restful Api###########################
from api.index import *

########################restful-中文###############################
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

########################注册蓝图###########################
from view import view_blue
app.register_blueprint(view_blue)


########################初始页面##########################
@app.route('/')
def index():
    return 'welcome to my api'


if __name__ == '__main__':
    app.run()