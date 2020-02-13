#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: liucheng
@contact: liucheng@memect.co
@file: app.py
@time: 2/12/20 9:48 PM
@desc:
"""
from sanic import Sanic
from sanic.response import json, file
import os
import hashlib
import pathlib


app = Sanic()
# 图片存储目录
parent_dir = str(pathlib.Path(__file__).resolve().parents[1])
base_dir = os.path.join(parent_dir, 'static/image')
# 校验 Token 写死就成，反正自己用的嘛
token = 'ChanEcho'
# 允许的域名列表
allow_host = [
    'localhost',
    'ilovechanecho',
]


# 成功返回方法
def ok(data):
    if type(data) == list:
        return json({"data": {"list": data}, "status": 0})
    else:
        return json({"data": data, "status": 0})


# 失败返回方法
def fail(data):
    return json({"data": data, "status": 1})


# 获取图片后缀名
def get_suffix(filename):
    temp_arr = filename.split('.')
    suffix = temp_arr[-1]
    file_type = ['jpg', 'jpeg', 'gif', 'png']
    if len(temp_arr) < 2:
        return 'error name'
    elif suffix not in file_type:
        return 'error type'
    else:
        return suffix


# 检查请求地址是否授权
def check_host(host):
    for i in allow_host:
        if i in host:
            return True
    return False


# 上传图片文件接口
@app.route('/api/upimg', methods=['POST'])
async def upimg(request):
    # 判断用户是否具有上传权限
    if request.headers.get('token') != token:
        return fail('Permission error')
    image = request.files.get('file').body
    # 判断文件是否支持
    image_name = request.files.get('file').name
    image_suffix = get_suffix(image_name)
    if 'error' in image_suffix:
        return fail(image_suffix)
    # 组织图片存储路径
    m1 = hashlib.md5()
    m1.update(image)
    md5_name = m1.hexdigest()

    # 用 md5 的前两位来建文件夹，防止单个文件夹下图片过多，又或者根目录下建立太多的文件夹
    save_dir = os.path.join(base_dir, md5_name[0:2])
    save_path = os.path.join(save_dir, md5_name[2:] + '.' + image_suffix)
    res_path = '/' + md5_name[0:2] + '/' + md5_name[2:] + '.' + image_suffix

    # 如果文件夹不存在，就创建文件夹
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 将文件写入到硬盘
    temp_file = open(save_path, 'wb')
    temp_file.write(image)
    temp_file.close()

    # 给客户端返回结果
    return ok({"path": res_path})


# 请求图片接口
@app.route('/api/img', methods=['GET'])
async def img(request):
    # 判断是否为网站请求，否则就加上自定义的字符串（允许本地访问）
    host = request.headers.get('referer') or 'ilovechanecho'
    # 判断请求接口是否带参数，否则加上自定义字符串（没有这个文件夹，返回404）
    args = request.args.get('path') or 'ilovexinyue'
    # 拼接文件地址
    path = base_dir + args
    # 如果不在允许列表，则展示 401 图片
    if not check_host(host):
        path = base_dir + '/d4/f187d215e76cef045d5901a640c447.png'
    # 如果文件不存在，则展示 404 图片
    if not os.path.exists(path):
        path = base_dir + '/d8/3355bb194482d837a18b85fd7d9cde.png'
    # 返回文件
    return await file(path)


# 启动服务
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
