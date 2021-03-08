import os
import sys
import json
import time
import datetime
from flask import request
from flask_restful import Resource
from flask_restful import reqparse, abort
from app import cache
from Logger import log
from utils.nlp.sentiment.index import getSentiment
from utils.other.token import checkTokenWrap


class Sentiment(Resource):
    @checkTokenWrap(cache=cache, request=request)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("text", type=str, required=True)
            args = parser.parse_args()
            text = args['text']
            # 首先从缓存中查找
            results = cache.get(text)
            if not results:
                results = getSentiment(text=text)
                if results is None:
                    return {
                        'status_code': 400,
                        'message': 'error in get sentiment'
                    }, 400
                else:
                    # 计算结果存入缓存
                    cache.set(text, results, 600)
                    return {
                        'status_code': 200,
                        'message': 'get sentiment successfully',
                        'data': results
                    }, 200
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
