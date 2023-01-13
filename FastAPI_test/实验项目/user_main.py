import hashlib
import uuid
from typing import Optional

import uvicorn
from fastapi import FastAPI, Query, Path, Body, Header
from pydantic import BaseModel, Field
from db import *
import uvicorn
from cache import *

# ！  C:\Users\熊健熹\AppData\Local\Programs\Python\Python310
# _*_ coding: UTF-8 _*_
'''
@Project :webservers
@File    :user_main.py
@Author  :magic007
@Date    : 15:03
'''

app = FastAPI(title='爱读书App接口服务',
              version='1.0',
              description='面向app,提交数据的API接口,包含会员、搜索、分类、活动、积分、评论、我的书架、广告等模块'
              )


# get /login?name=disen&pwd=123 http/1.1 请求报文的第一行
# name和pwd属于Query查询参数
@app.get('/login')
async def user_login_get(name: str = Query(..., min_length=4, max_length=20, regex=r'^[a-zA-Z]+$'),
                         pwd: str = Query(..., min_length=3, max_length=20)):
    ret = query('test_user', 'id', 'phone', 'nick_name', 'head', 'is_active',
                where='username=%s and auth_string=%s',
                args=(name, pwd), one=True)
    if ret:
        if not ret['is_active']:
            return {'msg': '当前用户未激活用户，请先激活用户', 'url': f'/active/{ret["id"]}'}
        ret['username'] = name
        ret['token'] = uuid.uuid4().hex
        # token和user_id 存到缓存中：
        save_token(ret['token'], ret['id'])
        return {'msg': '登录成功', 'data': ret}

    return {'msg': '登录失败，用户名或者口令错误', 'user': {
        'name': name,
        'pwd': pwd
    }}


# /active/2 基于url路径传参数： 路径参数Path
@app.get('/active/{user_id}')
def active_user(user_id: int = Path(..., ge=1)):
    ret = query('test_user', 'id', 'username', 'is_active',
                where='id=%s', args=(user_id,), one=True)
    if not ret:
        return {'msg': '要激活的用户不存在，请确认用户ID'}
    elif ret['is_active']:
        return {'msg': '用户已经激活'}
    else:
        save('test_user', id=user_id, is_active=1)
        if update('test_user', id=user_id, is_active=1):
            return {'msg': '用户激活成功，可以正常登录'}
    return {'msg': '用户激活失败'}


# 定制请求体body的模型类，期待json对象的属性
class UserInfo(BaseModel):
    nick_name: Optional[str] = Field(None, max_length=20,
                                     regex=r'[\u4e00-\u9fa5]+',
                                     title='中文的昵称')
    phone: Optional[str] = Field(None, regex=r'^1[3-9]\d{9}$',
                                 title='手机号')
    email: Optional[str] = Field(None, regex=r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$',
                                 title='邮箱')


@app.put('/user', name='更新用户', description='更新用户')
def update_user(token: Optional[str] = Header(..., title='请求头上的token'),
                user: UserInfo = Body(...)):
    # 实现业务功能
    # 1.验证token是否有效
    if not has_token(token):
        return {'msg': '这是一个无效的token，请重新登录'}
    # 2.toekn有效时，获取user_id
    user_id = get_user_id(token)
    if not query('test_user', 'id', where='id=%s and is_active=1', args=(user_id,), one=True):
        return {'msg': '当前用户状态异常，请联系管理员'}
    # 3.获取user_id的数据库中的数据或者生成更新数据的条件
    # 将BaseModel请求体的对象转成字典
    # 有可能自更新某一项，exclude_unset=True表示只获取请求体中存在的信息
    update_user = user.dict(exclude_unset=False)
    update_user['id'] = user_id  # 更新sql语句的条件
    print(update_user)
    # 4.调用db模块的save()或者updata()方法，完成数据库中的数据更新
    flag = update('test_user', **update_user)
    return {
        'msg': '用户更新成功' if flag else '用户更新失败'
    }


@app.get('/logout')
def logout(token: Optional[str] = Header(...)):
    remove_token(token)
    return {'msg': '用户退出成功'}


if __name__ == '__main__':
    uvicorn.run('user_main:app', host='127.0.0.1', port=8000, reload=True)
