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
from utils.spider.kuaishou import getKuaishou
from utils.other.token import checkTokenWrap


class KuaishouVideo(Resource):
    @checkTokenWrap(cache=cache, request=request)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cookie', type=str, required=True)
            parser.add_argument('user_id', type=str, required=True)
            parser.add_argument('pcursor', type=str, default=None)
            args = parser.parse_args()
            cookie = args['cookie']
            if not cookie or len(cookie) == 0:
                cookie = None
            user_id = args['user_id']
            pcursor = args['pcursor']
            if not pcursor or len(pcursor) == 0:
                pcursor = None
            results = getKuaishou(t='video',
                                  cookie=cookie,
                                  user_id=user_id,
                                  pcursor=pcursor)
            return results, results.get('status_code', 400)
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('ZhihuQuestion.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400


class KuaishouComment(Resource):
    @checkTokenWrap(cache=cache, request=request)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cookie', type=str, required=True)
            parser.add_argument('video_id', type=str, required=True)
            parser.add_argument('pcursor', type=str, default=None)
            args = parser.parse_args()
            cookie = args['cookie']
            if not cookie or len(cookie) == 0:
                cookie = None
            pcursor = args['pcursor']
            if not pcursor or len(pcursor) == 0:
                pcursor = None
            video_id = args['video_id']
            results = getKuaishou(t='comment',
                                  video_id=video_id,
                                  cookie=cookie,
                                  pcursor=pcursor)
            return results, results.get('status_code', 400)
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('ZhihuComment.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400


class KuaishouSearch(Resource):
    @checkTokenWrap(cache=cache, request=request)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cookie', type=str, required=True)
            parser.add_argument('kw', type=str, required=True)
            parser.add_argument('pcursor', type=str, default=None)
            args = parser.parse_args()
            cookie = args['cookie']
            if not cookie or len(cookie) == 0:
                cookie = None
            pcursor = args['pcursor']
            if not pcursor or len(pcursor) == 0:
                pcursor = None
            kw = args['kw']
            results = getKuaishou(t='search',
                                  kw=kw,
                                  cookie=cookie,
                                  pcursor=pcursor)
            return results, results.get('status_code', 400)
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('KuaishouSearch.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400