# coding:utf-8
import os
import sys
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from utils.other.des import *
from conf.config import Config

conf = Config()
file_path = conf.file_path


def rndColor():
    '''随机颜色'''
    return (random.randint(32,
                           127), random.randint(32,
                                                127), random.randint(32, 127))


def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)


def get_verify_code(code='1234'):
    '''生成验证码图形'''
    # code = gene_text()
    # code = code.lower()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 字体
    font = ImageFont.truetype(os.path.join(file_path, 'font/ARMOUREx_Md.ttf'),
                              30)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text(
            (5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
            text=code[item],
            fill=rndColor(),
            font=font)
    # 划线
    draw_lines(draw, 2, width, height)
    # 高斯模糊
    # im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
    return im


if __name__ == '__main__':
    print('root_path')
