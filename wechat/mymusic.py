# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
import base64
import struct
from binascii import b2a_hex
import requests
import json


#调用网易云音乐接口，涉及解密加密等操作

# 补全字符
def align(s):
    s = s.encode("utf-8")
    count = 16 - len(s) % 16
    c = bytes((count,))
    s = s + count * c
    return s


# CBC模式加密
def encrypt_CBC(str, key):
    # 补全字符串
    str = align(str)
    # 初始化AES，引入初始向量
    AESCipher = AES.new(key, AES.MODE_CBC, '0102030405060708')
    # 加密
    cipher = AESCipher.encrypt(str)
    return base64.b64encode(cipher)


def a(a):
    c = random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", a)
    return "".join(c)


def b(a, b):
    return encrypt_CBC(a, b)


def get_params(d):
    e = "010001"
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    g = "0CoJUm6Qyw8W8jud"
    i = 'a8LWv2uAtXjzSfkQ'
    h = b(d, g)
    h = b(h.decode('utf-8'), i)
    return h

def get_enc():
    return '2d48fd9fb8e58bc9c1f14a7bda1b8e49a3520a67a2300a1f73766caee29f2411c5350bceb15ed196ca963d6a6d0b61f3734f0a0f4a172ad853f16dd06018bc5ca8fb640eaa8decd1cd41f66e166cea7a3023bd63960e656ec97751cfc7ce08d943928e9db9b35400ff3d138bda1ab511a06fbee75585191cabe0e6e63f7350d6'


def get_info(song):
    url = "http://music.163.com/weapi/cloudsearch/get/web?csrf_token="
    header_dict = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    }
    params_str = "{\"s\":\"%s\",\"limit\":\"8\",\"csrf_token\":\"\"}" % song
    params = get_params(params_str)
    enc = get_enc()
    payload = {
        'params': params,
        'encSecKey': enc,
        'type': '1'
    }
    response = requests.post(url=url, headers=header_dict, data=payload)
    content = response.json()
    return content


def get_url(id):
    url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    header_dict = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    }

    params_str = "{\"ids\":\"[%s]\",\"br\":128000,\"csrf_token\":\"\"}" % id
    params = get_params(params_str)
    enc = get_enc()

    payload = {
        'params': params,
        'encSecKey': enc
    }
    response = requests.post(url=url, headers=header_dict, data=payload)
    content = response.json()
    return content['data'][0]['url']


def get_music(str):
    try:
        info = get_info(str)
        if (info['result']['songCount'] == 0):
            result_data = ['0']
            return result_data
        else:
            song = info['result']['songs'][0]
            id = song['id']
            name = song['name']
            ar = song['ar'][0]['name']
            music_url = get_url(id)
            result_data = ['1', name, ar, music_url]
            return result_data
    except:
        result_data = ['0']
        return result_data