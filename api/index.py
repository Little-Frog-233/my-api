from app import app
from flask_restful import Api

########################注册Restful Api###########################
from api.nlp.sentiment.index import *
from api.captcha.index import *
from api.user.index import *
api = Api(app)

###用户###
api.add_resource(UserRegister, '/api/user/register/')
api.add_resource(User, '/api/user/')

###sentiment###
api.add_resource(Sentiment, '/api/nlp/sentiment/')

###验证码###
api.add_resource(Captcha, '/api/captcha/')