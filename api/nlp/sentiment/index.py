import os
import sys
import json
import time
import datetime
from flask import request
from flask_restful import Resource
from flask_restful import reqparse, abort
# from app import cache
from Logger import log
from utils.nlp.sentiment.index import getSentiment


class Sentiment(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("text", type=str, required=True)
            args = parser.parse_args()
            text = args['text']
            results = getSentiment(text=text)
            if results is None:
                return {
                    'status_code': 400,
                    'message': 'error in get sentiment'
                }, 400
            else:
                return {
                    'status_code': 200,
                    'message': 'get sentiment successfully',
                    'data': results
                }, 200
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('Sentiment.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400

    def get(self):
        return {'status_code': 200, 'message': 'get your get'}
