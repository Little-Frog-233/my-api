import os
import sys
import json
import requests
from flask import session, request
# from app_back.newResource import NewResource as Resource
from flask_restful import Resource
from flask_restful import reqparse, abort
from app import cache
from utils.other.des import *
from utils.other.captcha import *
from conf.config import Config
from Logger import log

conf = Config()


class Captcha(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('captcha_token', type=str)
            parser.add_argument('captcha', type=str)
            args = parser.parse_args()
            captcha_token = args['captcha_token']
            captcha = args['captcha']
            log('Captcha.post').logger.info(
                'captcha: %s captcha_token_des: %s' %
                (captcha, des_descrypt(captcha_token)))
            if captcha.lower() == des_descrypt(captcha_token).lower():
                return {'status_code': 200, 'message': 'captcha right'}
            else:
                return {'status_code': 400, 'message': 'captcha wrong'}, 400
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('Captcha.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error'}, 400

    def get(self):
        code = gene_text()
        des_code = des_encrypt(code)
        url = conf.base_url + '/captcha/%s' % des_code
        return {
            'status_code': 200,
            'message': '',
            'data': {
                'url': url,
                'captcha_token': des_code
            }
        }
