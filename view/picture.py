import os
import sys
import configparser
import base64
import requests
from io import BytesIO
from flask import make_response, request, abort, redirect, url_for, session
from view import view_blue
from conf.config import Config
from utils.other.captcha import get_verify_code
from utils.other.des import *
from Logger import log
from PIL import Image
from app import cache

conf = Config()
file_path = conf.file_path

# logo保存路径
logo_path = conf.logo_path
# logo_url = conf.logo_url
# 用户图片保存路径
logouser_path = conf.logouser_path
# logouser_url = conf.logouser_url


@view_blue.route('/show/logo/<string:filename>', methods=['GET'])
def showLogo(filename):
    '''
    展示logo
    :param filename:
    :return:
    '''
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            try:
                logo_file_path = os.path.join(logo_path, filename)
                if not os.path.exists(logo_file_path):
                    return redirect(
                        url_for('view.showLogo', filename='upload_photo.jpg'))
                logo_file = open(logo_file_path, "rb").read()
                resp = make_response(logo_file)
                resp.content_type = 'image/%s' % filename.split('.')[-1]
                return resp
            except Exception as e:
                print(e)
                return redirect(
                    url_for('view.showLogo', filename='upload_photo.jpg'))
    else:
        pass


@view_blue.route('/show/logouser/<string:filename>', methods=['GET'])
def showLogouser(filename):
    '''
    展示用户头像
    :param filename: 文件名称
    :return:
    '''
    try:
        if not filename:
            return redirect(
                url_for('view.showLogo', filename='user_undefined.png'))
        if request.method == 'GET':
            try:
                logouser_file_path = os.path.join(logouser_path, filename)
                if not os.path.exists(logouser_file_path):
                    return redirect(
                        url_for('view.showLogo', filename='upload_photo.jpg'))
                logouser_file = open(logouser_file_path, "rb").read()
                resp = make_response(logouser_file)
                resp.content_type = 'image/%s' % filename.split('.')[-1]
                return resp
            except:
                return redirect(
                    url_for('view.showLogo', filename='user_undefined.png'))
        else:
            pass
    except Exception as e:
        return redirect(url_for('view.showLogo',
                                filename='user_undefined.png'))


@view_blue.route('/captcha/<string:code>')
def graph_captcha(code):
    code = des_descrypt(code)
    image = get_verify_code(code)
    out = BytesIO()  # 在内存中读写bytes
    image.save(out, 'png')
    image.close()
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp