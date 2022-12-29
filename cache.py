# ！  C:\Users\熊健熹\AppData\Local\Programs\Python\Python310
# _*_ coding: UTF-8 _*_
'''
@Project :webservers
@File    :cache.py
@Author  :magic007
@Date    : 9:13
'''
from redis import Redis
# 默认port=6379,db=0
_rds = Redis('centos', decode_responses=True)


# 保存token,建立token和user_id的绑定关系
def save_token(token, user_id):
    _rds.set(token, user_id)


# 根据token获取绑定的user_id
def get_user_id(token):
    return _rds.get(token)


# 验证token是否有效
def has_token(token):
    return _rds.exists(token)

# 思考：海量用户登出，如何删除token
def remove_token(token):
    if has_token(token):
        _rds.delete(token)
