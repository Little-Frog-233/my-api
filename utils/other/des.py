# coding:utf-8
from pyDes import des, CBC, PAD_PKCS5
import binascii

# 秘钥
KEY = 'mHAxsLYz'


def des_encrypt(s):
	"""
	DES 加密
	:param s: 原始字符串
	:return: 加密后字符串，16进制
	"""
	secret_key = KEY
	iv = secret_key
	k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
	en = k.encrypt(s, padmode=PAD_PKCS5)
	res = binascii.b2a_hex(en)
	res = res.decode('utf-8')
	return res


def des_descrypt(s):
	"""
	DES 解密
	:param s: 加密后的字符串，16进制
	:return:  解密后的字符串
	"""
	secret_key = KEY
	iv = secret_key
	k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
	de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
	if type(de) is not str:
		de = de.decode('utf-8')
	return de


if __name__ == '__main__':
	print(des_encrypt('zndex'))
	print(des_descrypt('f109601b211d8b09'))
