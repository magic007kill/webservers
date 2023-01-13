from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import List, Optional
from pathlib import Path

'''
1.使用Python的类型注解来进行数据校验和settings管理
2.Pydantic可以在代码运行时提供类型提示，数据校验失败时提供友好的错误提示
3.定义数据应该如何在纯规范的Python代码中保存，并用Pydantic验证它
'''


class User(BaseModel):
    id: int  # 没有默认值，为必填字段
    name: str = "John Snow"  # 有默认值，为选填字段
    signup_ts: Optional[datetime] = None  # Optional可以是字段为选填字段
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型


print('\033[31m1. ----------Pydantic的基本用法----------\033[0m')
external_data = {
    "id": "123",
    "signup_ts": "2022-12-30 10:54",
    "friends": [1, 2, "3"]
}
user = User(**external_data)
print(user.id, user.friends)
print(repr(user.signup_ts))
print(user.dict())

print('\033[31m2. ----------校验失败处理----------\033[0m')
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, 'no'])
except ValidationError as e:
    print(e.json())  # 把错误信息进行Json格式化

print('\033[31m3. ----------模型类的属性和方法----------\033[0m')
print(user.dict())
print(user.json())
print(user.copy())  # 这里是浅拷贝
print('-----------------------------------------------')
print(User.parse_obj(obj=external_data))
print(User.parse_raw('{"id": "123", "signup_ts": "2022-12-30 10:54", "iends": [1, 2, "3"]}'))
print('-----------------------------------------------')
path = Path('pydantic_test.json')
path.write_text('{"id": "123", "signup_ts": "2022-12-30 10:54", "iends": [1, 2, "3"]}')
print(User.parse_file(path))
Path('haha.txt').write_text('我是哈哈', encoding='utf-8')  # 可以使用Path函数创建文件，并向文件内写内容
print('-----------------------------------------------')
print(user.schema())
print(user.schema_json())

print(user.construct())