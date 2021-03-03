'''
所有对mysql的操作的函数
'''
import sys
import json
import datetime
from utils.other.des import *
from utils.mysql.models import User as _User
from utils.mysql.db import db
from conf.config import Config
from Logger import log

conf = Config()


def verifyUser(username, password):
    '''
    验证用户
    返回用户id
    '''
    try:
        user = _User.query.filter_by(username=username).first()
        if des_encrypt(password) == user.password:
            return (user.id, user.user_admin, user.manage)
        return None
    except Exception as e:
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.verifyUser').logger.error(msg)
        return False


def getUser(user_id):
    '''
    获取用户信息
    '''
    try:
        user = _User.query.filter_by(id=user_id).first()
        user_message = {}
        user_message['id'] = user.id
        user_message['username'] = user.username
        user_message['picture'] = user.userpicture
        user_message['picture_url'] = conf.logouser_url + user.userpicture
        user_message['admin'] = user.user_admin
        user_message['manage'] = user.manage
        return user_message
    except Exception as e:
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.verifyUser').logger.error(msg)
        return None


def checkUserName(username):
    '''
    检查用户名
    '''
    try:
        user = _User.query.filter_by(username=username).first()
        if user:
            return True
        return False
    except Exception as e:
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.checkUserName').logger.error(msg)
        return False


def getUserList(f="normal", user_id=None):
    '''
    f: normal(no manage) all(all)
    '''
    try:
        users = _User().query.all()
        user_list = []
        for user in users:
            user_message = {}
            user_message['id'] = user.id
            user_message['username'] = user.username
            user_message['picture'] = user.userpicture
            user_message['admin'] = user.user_admin
            if user_id is not None:
                if user_message['id'] == user_id:
                    continue
            if f == "normal":
                if user.manage != 1:
                    user_list.append(user_message)
            else:
                user_list.append(user_message)
        return user_list
    except Exception as e:
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.getuserList').logger.error(msg)
        return []


def addUser(username, password, userpicture, admin=0):
    '''
    新增用户
    '''
    try:
        user = _User()
        user.username = username
        user.password = des_encrypt(password)
        user.userpicture = userpicture
        user.user_admin = admin
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.addUser').logger.error(msg)
        return False


def deleteUser(user_id):
    '''
    删除用户
    '''
    try:
        user = _User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.deleteUser').logger.error(msg)
        return False


def updateUserPicture(user_id, userpicture):
    '''
    更新用户图片(已废除)
    '''
    try:
        user = _User.query.filter_by(id=user_id).first()
        user.userpicture = userpicture
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.updateUserPicture').logger.error(msg)
        return False


def updateUser(user_id, userpicture=None, user_admin=None):
    '''
    更新用户任务数据和图片
    '''
    try:
        user = _User.query.filter_by(id=user_id).first()
        if userpicture:
            user.userpicture = userpicture
        if user_admin is not None:
            user.user_admin = user_admin
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        log('mysql.tools.updateUserTask').logger.error(msg)
        return False