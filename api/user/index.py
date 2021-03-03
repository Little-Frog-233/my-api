import os
import sys
import json
import datetime
from flask import session, request
# from app_back.newResource import NewResource as Resource
from flask_restful import Resource
from flask_restful import reqparse, abort
from app import cache
from utils.mysql.tools import *
from utils.other.token import generateToken, checkTokenWrap, refreshToken, desToken, deleteToken
from Logger import log


class UserRegister(Resource):
    def get(self):
        return {'status_code': 400, 'message': 'bad request'}, 400

    def post(self):
        '''
        新增用户
        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('userpicture',
                                type=str,
                                default='user_undefined.png')
            parser.add_argument('admin', type=int, default=0)
            args = parser.parse_args()
            username = args['username']
            password = args['password']
            userpicture = args['userpicture']
            admin = args['admin']
            if checkUserName(username=username):
                return {'status_code': 400, 'message': '用户名已经存在'}, 400
            if addUser(username=username,
                       password=password,
                       userpicture=userpicture,
                       admin=admin):
                return {'status_code': 200, 'message': 'add_successfully'}
            return {'status_code': 400, 'message': 'add fail'}, 400
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('UserRegister.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400


class User(Resource):
    '''
    前后端分离的用户验证
    前端请求，headers需带上accept-token，值为用户验证之后生成的token
    '''
    def post(self):
        '''
        验证用户登陆
        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()
            username = args['username']
            password = args['password']
            token = generateToken(cache=cache,
                                  request=request,
                                  username=username,
                                  password=password)
            if token is not None:
                return {
                    'status_code': 200,
                    'message': '登陆成功',
                    'data': {
                        'token': token
                    }
                }
            else:
                return {'status_code': 400, 'message': '用户名和密码不匹配'}, 400
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('User.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400

    @checkTokenWrap(cache=cache, request=request)
    def get(self):
        '''
        获取用户信息
        每次获取，更新cache
        '''
        try:
            token = request.headers.get('accept-token')
            user_message_temp = desToken(token=token)
            ###更新缓存时间
            refreshToken(cache=cache, request=request)
            # 返回用户信息
            user_id = user_message_temp['id']
            user_message = getUser(user_id=user_id)
            return {
                'status_code': 200,
                'message': '',
                'data': {
                    'user_message': user_message
                }
            }
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('User.get').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400

    @checkTokenWrap(cache=cache, request=request)
    def put(self):
        '''
        更新用户数据
        图片 + 任务数
        '''
        try:
            token = request.headers.get('accept-token')
            user_message_temp = desToken(token)
            user_id = user_message_temp['id']
            parser = reqparse.RequestParser()
            parser.add_argument('picture', type=str, default=None)
            args = parser.parse_args()
            picture = args['picture']
            if not picture or len(picture) <= 0:
                picture = None
            if updateUser(user_id=user_id, userpicture=picture):
                return {'status_code': 200, 'message': '更新成功'}
            return {'status_code': 400, 'message': 'error happened'}, 400
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('User.put').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400

    @checkTokenWrap(cache=cache, request=request)
    def delete(self):
        '''
        退出登录
        '''
        try:
            deleteToken(cache=cache, request=request)
            return {'status_code': 200, 'message': '退出登陆成功'}
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('User.delete').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400


class UserList(Resource):
    @checkTokenWrap(cache=cache, request=request, need_admin=True)
    def get(self):
        '''
        获取用户列表
        当不提供page和size时，为获取全部用户列表
        filter: 'normal': 获取非manage 'all': 获取全部
        '''
        try:
            token = request.headers.get('accept-token')
            user_message_temp = desToken(token)
            user_id = user_message_temp['id']
            parser = reqparse.RequestParser()
            parser.add_argument('page', type=int)
            parser.add_argument('size', type=int)
            parser.add_argument('filter', type=str, default="normal")
            args = parser.parse_args()
            page = args['page']
            size = args['size']
            f = args['filter']
            user_list = getUserList(f=f, user_id=user_id)
            if page and size:
                total = len(user_list)
                start = (page - 1) * size
                end = page * size
                if end >= total:
                    more = False
                else:
                    more = True
                user_list = user_list[start:end]
            else:
                total = len(user_list)
                more = False
            return {
                'status_code': 200,
                'message': '',
                'data': {
                    'user_list': user_list,
                    'total': total,
                    'more': more
                }
            }
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('UserList.get').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400

    @checkTokenWrap(cache=cache,
                    request=request,
                    need_admin=True,
                    need_manage=True)
    def post(self):
        '''
        更新用户权限
        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int)
            parser.add_argument('admin', type=int, default=0)
            args = parser.parse_args()
            user_id = args['user_id']
            admin = args['admin']
            if updateUser(user_id=user_id, user_admin=admin):
                return {'status_code': 200, 'message': '更新成功'}
            else:
                return {'status_code': 400, 'message': '更新失败'}, 400
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('UserList.post').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400

    @checkTokenWrap(cache=cache,
                    request=request,
                    need_admin=True,
                    need_manage=True)
    def delete(self):
        '''
        删除用户
        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int)
            args = parser.parse_args()
            user_id = args['user_id']
            if deleteUser(user_id=user_id):
                return {'status_code': 200, 'message': '删除成功'}
            else:
                return {'status_code': 400, 'message': '删除失败'}, 400
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            log('UserList.delete').logger.error(msg)
            return {'status_code': 400, 'message': 'error happened'}, 400
