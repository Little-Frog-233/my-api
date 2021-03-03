import json
import datetime
from functools import wraps
from utils.mysql.tools import *
from utils.other.des import des_descrypt


def generateToken(cache, request, username, password):
    '''
    产生token的逻辑
    '''
    user_result = verifyUser(username=username, password=password)
    if user_result:
        user_message = {
            'id': user_result[0],
        }
        token = {
            'id': user_result[0],
            'user-agent': request.headers.get('User-Agent', '111'),
            'create_time':
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        token = des_encrypt(json.dumps(token, ensure_ascii=False))
        ###设置缓存
        cache.set(token, user_message, timeout=604800)
        return token
    return None


def desToken(token):
    '''
    解析token
    '''
    token_message = json.loads(des_descrypt(token))
    return token_message


def checkToken(token, cache, request, need_admin=False, need_manage=False):
    '''
    验证token是否有效
    有效则返回user_message的token
    need_admin: 需要用户为admin才能有效
    need_manage: 需要用户为manage才能有效
    权限每次都从数据库中获取，保证热更新
    user_message: {
        'id': int
    }
    '''
    try:
        token_message = json.loads(des_descrypt(token))
        if token_message['user-agent'] != request.headers.get(
                'User-Agent', '111'):
            return None
        user_message = cache.get(token)
        ###验证缓存的登陆状态
        if not user_message:
            return None
        ###验证用户是否存在
        user_id = user_message['id']
        message_verify = getUser(user_id=user_id)
        if not message_verify:
            return None
        # user_message = message_verify
        ###验证用户是否为管理员(可进行操作)
        if need_admin:
            if message_verify.get('admin', 0) != 1:
                return None
        if need_manage:
            if message_verify.get('manage', 0) != 1:
                return None
        # cache.set(token, user_message, timeout=604800)
        return user_message
    except Exception as e:
        return None


def checkTokenCode(token, cache, request, need_admin=False, need_manage=False):
    '''
    验证token是否有效
    返回code, message
    100: token错误
    200: 正常
    300: 登录过期
    400: 用户不存在
    500: 权限不够
    600: 未知错误
    '''
    try:
        token_message = json.loads(des_descrypt(token))
        if token_message['user-agent'] != request.headers.get(
                'User-Agent', '111'):
            return 100, '登陆错误'
        user_message = cache.get(token)
        ###验证缓存的登陆状态
        if not user_message:
            return 300, '登录过期'
        ###验证用户是否存在
        user_id = user_message['id']
        message_verify = getUser(user_id=user_id)
        if not message_verify:
            return 400, '用户不存在'
        # user_message = message_verify
        ###验证用户是否为管理员(可进行操作)
        if need_admin:
            if message_verify.get('admin', 0) != 1:
                return 500, '权限不够'
        if need_manage:
            if message_verify.get('manage', 0) != 1:
                return 500, '权限不够'
        # cache.set(token, user_message, timeout=604800)
        return 200, '正常'
    except Exception as e:
        return 600, '未知错误'


def refreshToken(cache, request):
    token = request.headers.get('accept-token')
    user_message = cache.get(token)
    cache.set(token, user_message, timeout=604800)
    return


def deleteToken(cache, request):
    token = request.headers.get('accept-token')
    cache.delete(token)
    return


def checkTokenWrap(cache, request, need_admin=False, need_manage=False):
    '''
    检查用户权限的装饰器
    用于restful请求中
    '''
    def checkWrapper(f):
        '''
        带参数
        '''
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('accept-token')
            if not token:
                return {'status_code': 400, 'message': '请求非法'}, 400
            code, msg = checkTokenCode(token=token,
                                       cache=cache,
                                       request=request,
                                       need_admin=need_admin,
                                       need_manage=need_manage)
            if code == 200:
                return f(*args, **kwargs)
            else:
                return {'status_code': 400, 'message': msg}, 400

        return wrapper

    return checkWrapper
