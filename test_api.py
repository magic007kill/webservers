# ！  C:\Users\熊健熹\AppData\Local\Programs\Python\Python310
# _*_ coding: UTF-8 _*_
'''
@Project :webservers
@File    :test_api.py
@Author  :magic007
@Date    : 14:36
'''
import requests

headers = {
        'token': 'affb3cfa1b9d41bd8acb1f7879d60dc8'
    }

def test_update():
    url = 'http://127.0.0.1:8000/user'
    body = {
        "nick_name": "小往",
        "phone": "18159859652",
        "email": "magic@qq.com"
    }

    resp = requests.put(url=url, json=body, headers=headers)
    print(resp.status_code)
    print(resp.json())
    return {'msg': '测试更改数据完成'}


def test_logout():
    url = 'http://127.0.0.1:8000/logout'
    resp = requests.get(url=url, headers=headers)
    print(resp.json())
    return {'msg': '测试登出完成'}


print(test_update())

