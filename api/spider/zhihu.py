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
from utils.spider.zhihu import getZhihu
from utils.other.token import checkTokenWrap


class ZhihuQuestion(Resource):
    @checkTokenWrap(cache=cache, request=request)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('kw', type=str, required=True)
            parser.add_argument('page', type=int, default=1)
            args = parser.parse_args()
            kw = args['kw']
            page = args['page']
            results = getZhihu(type='question', page=page, kw=kw)
            if results is None:
                return {
                    'status_code': 400,
                    'message': 'error in spider request'
                }, 400
            return {'status_code': 200, 'message': '', 'data': results}
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('ZhihuQuestion.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400


class ZhihuAnswer(Resource):
    @checkTokenWrap(cache=cache, request=request)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('q_id', type=str, required=True)
            parser.add_argument('page', type=int, default=1)
            args = parser.parse_args()
            q_id = args['q_id']
            page = args['page']
            results = getZhihu(type='answer', page=page, question_id=q_id)
            if results is None:
                return {
                    'status_code': 400,
                    'message': 'error in spider request'
                }, 400
            return {'status_code': 200, 'message': '', 'data': results}
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('ZhihuAnswer.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400