from app import app
from flask_restful import Api

########################注册Restful Api###########################
from api.nlp.sentiment.index import *
api = Api(app)

###sentiment###
api.add_resource(Sentiment, '/api/nlp/sentiment/')