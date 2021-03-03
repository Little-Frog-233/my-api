#coding:utf-8
import os
import sys
import json
from flask import session, request, Response
from werkzeug import secure_filename
from view import view_blue
from pypinyin import lazy_pinyin
from utils.other.token import checkToken
from utils.other.picture import getSmallPictureTools
from conf.config import Config
from utils.mysql.tools import *
from app import cache

conf = Config()
data_path = conf.file_path

user_logo_path = conf.logouser_path
user_logo_url = conf.logouser_url


@view_blue.route('/upload/user/logo/', methods=['POST', 'GET'])
def uploadUserLogo():
    '''

    :return:
    '''
    try:
        token = request.headers.get('accept-token')
        user_message = checkToken(token=token, cache=cache, request=request)
        if not user_message:
            resp = {'status_code': 400, 'message': '请求非法'}
            return Response(json.dumps(resp, ensure_ascii=False),
                            mimetype='application/json',
                            status=400)
        user_id = user_message['id']
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(''.join(lazy_pinyin(file.filename)))
            if '.jpg' in filename:
                filename = filename.replace('.jpg', '.png')
            if '.jpeg' in filename:
                filename = filename.replace('.jpeg', '.png')
            file_save_path = os.path.join(user_logo_path, filename)
            file.save(file_save_path)
            getSmallPictureTools(file_old=file_save_path,
                                 file_new=file_save_path,
                                 length=128)
            updateUser(user_id=user_id, userpicture=filename)
            message = 'upload file %s successfully' % filename
            resp = {
                "filename": filename,
                "file_url": user_logo_url + filename,
                'status_code': 200,
                'message': message
            }
            return Response(json.dumps(resp, ensure_ascii=False),
                            mimetype='application/json')
        else:
            resp = {'status_code': 400, 'message': 'get your get~'}
            return Response(json.dumps(resp, ensure_ascii=False),
                            mimetype='application/json',
                            status=400)
    except Exception as e:
        msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
        resp = {'status_code': 400, 'message': msg}
        return Response(json.dumps(resp, ensure_ascii=False),
                        mimetype='application/json',
                        status=400)
