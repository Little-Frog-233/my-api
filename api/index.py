from app import app
from flask_restful import Api

########################注册Restful Api###########################
from api.nlp.sentiment.index import *
from api.captcha.index import *
from api.user.index import *
from api.spider.zhihu import *
api = Api(app)

###用户###
api.add_resource(UserRegister, '/api/user/register/')
api.add_resource(User, '/api/user/')

###sentiment###
api.add_resource(Sentiment, '/api/nlp/sentiment/')

###spider###
#zhihu#
api.add_resource(ZhihuQuestion, '/api/spider/zhihu/question/')
api.add_resource(ZhihuAnswer, '/api/spider/zhihu/answer/')

###验证码###
api.add_resource(Captcha, '/api/captcha/')