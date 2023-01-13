import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# RESTful 接口设计规范中：
# 1. 面向资源（URI->url）
# 2.每一个资源都具有GET/POST/PUT/DELETE 四个标准动作(请求方法)
# 3.每个资源动作都是无状态的(HTTP协议的短连接，即不保存客户端和服务端的连接通道)
# 4. (C或B/S 客户端和服务端)交互的数据格式都使用json(content-type: application/json)

@app.get('/')
async def index():
    # 业务处理

    # 处理结果
    return {'data': ['disen', 'jack', 'lucy']}



# 基于BaseModel定义请求体的结构(json对象)
class LoginUser(BaseModel):
    phone: str
    code: str


class UsernameAndPassword(BaseModel):
    username: str  # 必填项
    password: str  # 必填项
    is_save: bool = False  # 可选项


@app.post('/login')
def user_login_by_phone(user: LoginUser):
    # 查询phone是否存在

    # 验证code是否有效

    return {'msg': '用户已登录', 'phone': user.phone}


@app.post('/login2')
async def user_login_by_username(user: UsernameAndPassword):
    print('--->', user)
    return {'msg': f'用户登录失败，此用户,{user.username}用户不存在'}


if __name__ == '__main__':
    uvicorn.run(app)
